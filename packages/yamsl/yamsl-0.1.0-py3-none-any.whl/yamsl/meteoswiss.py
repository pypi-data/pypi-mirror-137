from datetime import datetime
import locale
import logging
import aiohttp


class MeteoSwiss:
    
    baseUrl = "http://www.meteoschweiz.admin.ch"
    homePage = "home.html?tab=overview"

    forecastUrlPrefix = "/product/output/forecast-chart/version__"
    forecastUrlSuffix = ".json"

    locationUrlPrefix = "/etc.clientlibs/internet/clientlibs/meteoswiss/resources/ajax/location/"
    locationUrlSuffix = ".json"

    headersForRequests = {'User-Agent': 'Mozilla/5.0'}

    utcOffset = 0
    days = 0
    data = {}     


    async def setup(self, zipcode):
        self.zipcode = zipcode

        try:
            self.cityName = await self.getCityName()
        except Exception as e:
            raise Exception("Failed to get City name: %s" % e)


    async def updateForecast(self):
        try:
            forecastUrl = await self.getForecastUrl()
        except Exception as e:
            raise Exception("An error occured: %s" % e)

        try:
            forecastData = await self.collectData(dataUrl=forecastUrl)
        except Exception as e:
            raise Exception("An error occured: %s" % e)

        return forecastData
        


    async def getForecastUrl(self):
        async with aiohttp.ClientSession() as session:
            homePageUrl = self.baseUrl + "/" + self.homePage
            try:
                async with session.get(homePageUrl, headers=self.headersForRequests) as response:
                    homePageContent = await response.text()
            except Exception as e:
                raise Exception("Failed to fetch home page: %s" % e)

            forecastUrlStart = homePageContent.find(self.forecastUrlPrefix)
            forecastUrlEnd = homePageContent.find(self.forecastUrlSuffix, forecastUrlStart)
            if forecastUrlStart == -1:
                raise Exception("Failed to find Data URL prefix (\"%s\") in index URL (\"%s\")" % (self.forecastUrlPrefix, homePageUrl))
            if forecastUrlEnd == -1:
                raise Exception("Failed to find Data URL suffix (\"%s\") in index Page (\"%s\")" % (self.forecastUrlSuffix, homePageUrl))

            forecastUrl = self.baseUrl + "/" + homePageContent[forecastUrlStart:forecastUrlEnd - 6] + str(self.zipcode) + "00" + self.forecastUrlSuffix

            return forecastUrl



    async def getCityName(self):
        async with aiohttp.ClientSession() as session:
            locationUrl = self.baseUrl + self.locationUrlPrefix + str(self.zipcode) + "00" + self.locationUrlSuffix
            try:
                async with session.get(locationUrl, headers=self.headersForRequests) as response:
                    locationData = await response.json()
            except Exception as e:
                raise Exception("Failed to fetch forecast URL (\"%s\"): \"%s\"" % (locationUrl, e))

            return locationData["city_name"]

    

    async def collectData(self, dataUrl=None, daysToUse=7, timeFormat="%H:%M", dateFormat="%A, %d. %B", localeAlias="en_US.utf8"):
        self.data["dataUrl"] = dataUrl
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(dataUrl, headers={'User-Agent': 'Mozilla/5.0', 'referer': self.baseUrl + "/" + self.homePage}) as response:
                    forecastData = await response.json()
            except Exception as e:
                raise Exception("Failed to fetch data URL (%s): %s" % (dataUrl, e))

            self.days = len(forecastData)

            if daysToUse != None:
                if self.days < daysToUse:
                    daysToUse = self.days
                if self.days != daysToUse:
                    logging.debug("But going only to use the first %d days" % daysToUse)
                self.days = daysToUse

            dayNames = []
            formatedTime = []
            timestamps = []
            rainfall = []

            logging.debug("Parsing data...")

            try:
                locale.setlocale(locale.LC_ALL, localeAlias)
            except Exception as e:
                logging.warning("Unable to uses locale \"%s\": %s" % (localeAlias, e))

            for day in range(0, self.days):

                # get timestamps (the same for all data)
                for hour in range(0, 24):
                    try: # Last day might not have 24h
                        #print(day, hour)
                        timestamp = forecastData[day]["rainfall"][hour][0]
                        timestamp = int(int(timestamp) / 1000) + self.utcOffset * 3600
                    except:
                        logging.warning("For day %d only data of %d hours are provided!" % (day, hour))
                        timestamp = timestamps[-1] + 3600 # Use timstamp of last hour and add 3600 seconds
                    timestamps.append(timestamp)

            dayIndex = 0
            for timestamp in timestamps:
                formatedTime.append(datetime.fromtimestamp(timestamp).isoformat())
            rainfall = self.dataExtractorNormal(forecastData, self.days, "rainfall", 1)
            sunshine = self.dataExtractorNormal(forecastData, self.days, "sunshine", 1)
            temperature = self.dataExtractorNormal(forecastData, self.days, "temperature", 1)
            rainfallVarianceMin, rainfallVarianceMax = self.dataExtractorWithVariance(forecastData, self.days, "variance_rain", 1, 2)
            temperatureVarianceMin, temperatureVarianceMax = self.dataExtractorWithVariance(forecastData, self.days, "variance_range", 1, 2)
            wind = self.dataExtractorWithDataInSubfield(forecastData, self.days, "wind", "data", 1)
            windGustPeak = self.dataExtractorWithDataInSubfield(forecastData, self.days, "wind_gust_peak", "data", 1)


            for i in range(len(timestamps)):
                self.data[timestamps[i]] = {
                    "datetime": formatedTime[i],
                    "temperature": temperature[i],
                    "wind_speed": wind[i],
                    "rainfall": rainfall[i],
                    "temperatureVarianceMin": temperatureVarianceMin[i],
                    "temperatureVarianceMax": temperatureVarianceMax[i],
                    "windGustPeak": windGustPeak[i]
                    }


            logging.debug("All data parsed")

            return self.data


    def dataExtractorNormal(self, forecastData, days, topic, index):
        topicData = []
        for day in range(0, days):
            for hour in range(0, 24):
                try:
                    topicData.append(forecastData[day][topic][hour][index])
                except:
                    logging.warning("For day %d only %s data of %d hours are provided!" % (day, topic, hour))
                    topicData.append(None)
        return topicData


    """
    Extracts the data when it is placed in a sub-field
    """
    def dataExtractorWithDataInSubfield(self, forecastData, days, topic, subField, index):
        topicData = []
        for day in range(0, days):
            for hour in range(0, 24):
                try:
                    topicData.append(forecastData[day][topic][subField][hour][index])
                except:
                    logging.warning("For day %d only %s data of %d hours are provided!" % (day, topic, hour))
                    topicData.append(None)
        return topicData


    """
    Extracts the data with a min/max value
    """
    def dataExtractorWithVariance(self, forecastData, days, topic, indexMin, indexMax):
        topicDataMin = []
        topicDataMax = []
        for day in range(0, days):
            for hour in range(0, 24):
                try:
                    topicDataMin.append(forecastData[day][topic][hour][indexMin])
                    topicDataMax.append(forecastData[day][topic][hour][indexMax])
                except:
                    logging.warning("For day %d only %s data of %d hours are provided!" % (day, topic, hour))
                    topicDataMin.append(None)
                    topicDataMax.append(None)
        return [topicDataMin, topicDataMax]


    """
    Extracts the symbols
    """
    def dataExtractorSymbols(self, forecastData, days, topic, indexTS, indexId):
        timestamps = []
        ids = []
        for day in range(0, days):
            for index in range(0, 8):
                timestamp = forecastData[day][topic][index][indexTS]
                timestamps.append(int(int(timestamp) / 1000) + self.utcOffset * 3600)
                ids.append(forecastData[day][topic][index][indexId])
        return [timestamps, ids]
