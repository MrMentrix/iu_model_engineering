# Background Information
As one of the data scientists in an American public transport company, the logistic team ask you for help. They want to optimize the usage of the company's resources (the vehicles/taxis) by covering places with high demand for public transport. You should help them to predict the most important clusters for public transport (using taxis) as well as their progression over the day. To this end the logistic team gives you a dataset of the GPS data and starting time of the company's vehicles over the last six months. Use this data to create a regression model, possibly multiple ones, to predict the average demand of taxis per hour over the day in the ten most important clusters in the city. Discuss possible demand variability and propose a suitable prediction approach.
**Task:** Support the logistic team in the company with a prediction approach for the average demand of taxis per hour over the day in the ten most important clusters of the available data.
### 1. Business Understanding
We have a taxi company that wants to use prediction algorithms to improve the company's resource usage, i.e., have more taxis driving people and less taxis waiting for people. Therefore, we want to understand when and where people usually need and don't need taxis to position/deploy the taxis more effectively. This is not only an improvement for the business itself, but also for the customers as their needs will be better met.
### 2. Data Understanding & 3. Data Preparation
*Since Data Understanding goes hand in hand with Data Preparation, the two steps will be performed simultaneously, to understand the data better by preparing it for a first impression/analysis and using this newfound understanding to better prepare the data.*
###### First Data Understanding
The data is not very extensive, but sufficient. There are individual data sets from April 2014 until September 2014. The data includes coordinates and timestamps, the "Base" column is essentially useless, as it only repeats the same value and provides no real information. Therefore, all information available is where and when taxis are used. Unfortunately, there is no information regarding if a customer called a taxi to a given location or just entered it upon sight. Also, it is unclear how many taxis have been deployed at certain areas during certain times or how long a taxi has been occupied. Therefore, the actual demand is unclear as the data might be biased due to induced demand, i.e., more taxis lead to more people using taxis. For sake of the task, this will be ignored.
Upon exploring the data, it is very apparent that the overall demand, regardless of position, follows a clear pattern and could most likely be modeled using harmonic regression. The data seems to be quite clean.
###### Turning CSV into SQL
For many reasons, the .csv files will be combined into one large SQL Database using the sqlite3 library provided by Python. A few of the reasons are better latency and much easier working given that working with an SQL database is much more superior to working with several .csv files. It will also come in handy when retrieving specific subsets of the data. During this process, **all null values were removed**.

There might also be a seasonal component to the use of taxis, since the use of taxis vary greatly between months:
April: ~565k
May: ~652k
June: ~664k
July: ~796k
August: ~830k
September: ~1028k
Unfortunately, since only 6 months are provided, it is unclear what the harmonic pattern of this is. There might be higher use during certain seasons. Since it cannot be known for sure as much more data would be needed, we will assume a base level of ~750k passengers per month and adjust with an parameter $a$, where $a=\frac{month\_total}{\sigma}$, with $\sigma$ being defined as $750k$, $k$ being used as a denotation for "kilo" or "thousand". So for April, $a$ would be:

$a_{april}=\frac{565k}{750k}=0,753$. 

This way, all data can be used to train the models with to gain a larger understanding. Additionally, smaller, monthly models will be created to determine whether or not the hot spots for traffic/demand differ significantly between months.
###### Splitting Date Column
There is a reasonable assumption that there might be daily patterns in taxi demands, such as at the start or end of workdays. To better analyze this, the "Date/Time" column will be split up into a "date" and "time" column. This way, it will be much easier to retrieve data points from all days during all months between, e.g., 12:00 and 13:00.
###### Visualization
The visualization of the data does support this assumption as a clear decrease throughout the night, one local peak around 7:30 and another peak around 18:00 are very visible. This supports the assumption that there is a high demand for taxis at the start and the end of workdays. Of course, weekdays and weekends are combined in this visualization. However, the pattern is still clearly visible.
![[15_minutes.png]]
*Visualization of the sum of taxis being used/called over the entire 6-month period in 15-minute intervals from 00:00 to 23:59, regardless of date or location.*
### 4. Model Engineering
As the task asks for the 10 most important clusters, the clustering algorithm will be used to create 25 clusters. 7 Models will be created, each with the same architecture, but fitted to different data, namely to the one total/combined dataset, and to each individual monthly dataset. Then, the top 10 cluster centers will be compared to each other, determining if there is a significant difference regarding location based taxi demand between the individual months. If there is not, the 6 monthly models will be omitted and one combined model will be used. Otherwise, 6 monthly models will be used and the combined model will be omitted.