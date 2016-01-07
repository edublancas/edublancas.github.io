# Projects

These are some of my projects.

## Blight Prevention: Building Strong and Healthy Neighborhoods in Cincinnati

Center for Data Science and Public Policy, The University of Chicago. November 2015.

**Supervisors**

Rayid Ghani (The University of Chicago)

**Overview** (Taken from [DSSG website](https://www.google.com/url?q=http://dssg.uchicago.edu/project/proactive-blight-reduction-and-neighborhood-revitalization/&sa=D&usg=AFQjCNHlCm0by6KZOm074FlpKRe0ZCTY-Q))

Today, Cincinnati struggles with aging home stock, stifling economic redevelopment in some neighborhoods. Current efforts to enforce the building code citywide are largely reactive, driven by citizen complaints and often occurring too late to salvage the property. Going forward, the city wants to use data to identify declining properties before they endanger public safety and economic development, so that early intervention strategies can prevent further damage and stimulate neighborhood revitalization.

The Center for Data Science and Public Policy at The University of Chicago is continuing the DSSG summer project, which developed a system that identifies properties at risk of code violations or abandonment which do not have registered complaints, so that Cincinnati can proactively deploy inspectors to these buildings. The system will also identify which of the city’s blight reduction programs are most suited to address specific properties, helping city departments prioritize limited enforcement and legal resources for building code enforcement and rehabilitation.

**Contributions**

Building upon the original summer project, I revamped the data pipeline to make it reproducible and easy to use. The new version can be deployed using Docker. I’m currently working on adding more datasets to the pipeline as well as generating new features to improve the model. The pipeline uses Python for analysis and Bash to automate data acquisition, transformation and loading clean datasets to our PostgresQL database.

------

## Reducing Home Abandonment in Mexico

Data Science for Social Good Fellowship, The University of Chicago. May 2015.

**Supervisors**

Romana Khan, Ph.D. (Northwestern University), Paul van der Boor, Ph.D. (McKinsey & Company) and Rayid Ghani (The University of Chicago)

**Overview** (Taken from [DSSG website](https://www.google.com/url?q=http://dssg.uchicago.edu/project/improving-long-term-financial-soundness-by-identifying-causes-of-home-abandonment-in-mexico/&sa=D&usg=AFQjCNFqYFCl1G30NBKoZ6bJFtYiIGSSsw))

Infonavit is the largest provider of mortgages in Mexico, assisting lower-income families that cannot obtain financing from a private institution with acquisition and other housing solutions. Infonavit’s main objective is to increase the quality of life and equity value of Mexican workers and their families through two mandates: providing housing finance and managing workers’ savings. To advance this mission, the organization wants to understand the relationship between policy, social influences, and dwelling abandonment.

Our project will build upon preliminary results by exploring data from Infonavit, census and home surveys, loans, and social research to discover the factors that most elevate the risk of housing abandonment. DSSG will incorporate these findings into tools and evidence-based recommendations, helping Infonavit offer services and support local policy to mitigate abandonment and improve economic outcomes for the citizens of Mexico. These results may also support better housing value and credit origination for workers, as well as improve portfolio risk management and collection performance for Infonavit so that they can best accomplish their social mission.

**Contributions**

During the first month of the project, I was in charge of cleaning census datasets, I did most of that work using R. Once we had all our data in place, every member of the team tried different approaches and features to improve our models, we used Python and scikit-learn for training. Finally, to provide an interactive way for our partner to use the results, I developed a web application using Flask that estimated home abandonment for the next year given location and loan characteristics. Our results were presented in Data for Good Exchange, an event organized by Bloomberg in September 2015.

------

## SmartSit

Tecnológico de Monterrey in collaboration with University of Valencia, OHL, Indra and humaniks. January 2015.

**Supervisors**

Dr. Raúl Crespo Saucedo (Tecnológico de Monterrey) and Dr. Alfredo Victor Mantilla Caeiros (Tecnológico de Monterrey)

**Overview** (Taken from [Indra’s website](https://www.google.com/url?q=http://www.indracompany.com/en/sostenibilidad-e-innovacion/proyectos-innovacion/smartsit-resistive-magnetic-sensors-intelligent-tra&sa=D&usg=AFQjCNEBaG2Inlu58Ekz0K1LFI4WLkTBSg))

The project is focused in the development of systems for sensoring, based in the magnetic characteristics of the vehicles, improving currents methods to obtain traffic parameters and characterizing the vehicles when driving in the road. As result of the project it is expected to obtain a solution capable of replace and/or complement current traffic systems solutions, allowing:

-   Counting vehicles, traffic flow, traffic density, punctual speed, detection of driving direction
-   Vehicle re-identification, allowing to obtain travelling times, mean speeds in stretches, O/D Matrixes
-   Axel-counting in free-flow conditions

**Contributions**

My responsibility for this project was to evaluate WSN (Wireless Sensor Network) equipment, taking into account the project specifications. During four months, my teammate and I evaluated the SmartMesh WirelessHART equipment in different conditions and stress scenarios. We collected and then analyzed data to deliver a reliable diagnostic. The work involved developing an embedded system programmed using C. Data collection was made using a modified version of the manufacturer’s Python SDK. Data analysis was also done with Python and the Scientific Python stack.

---

## GobMX

Krieger Electronics and the Federal Government of Mexico. September 2014.

**Overview**

In September 2014, the Federal Government of Mexico launched a challenge to develop a mobile application that would serve citizens to ease legal paperwork. Krieger Electronics entered in such competition and I worked with them as a consultant, due to my prior experience working with government agencies to use mobile technology to improve public services. My team won the challenge and was granted a contract to develop the final product, this was one of the first contracts signed as a result of an open and transparent competition. The  first version was released in early 2016 to millions of citizens all across the country.

**Contributions**

I helped the team to scope the prototype in terms features and user experience. When we started the development I was in charge of our search engine, a feature that helps users find paperwork requirements using common language instead of formal terminology used by government officials. To do that, I scraped website to build a corpus of more than 3,500 paperwork procedures and build the engine using td-idf term weighting.

---

## Fritime

Mexico City. January 2014.

**Overview**

Fritime is a startup that developed a mobile application to let groups of friends find new venues based on their common interests using AI. We got seed funding from private investors.

**Contributions**

During the first year I was in charge of the entire software stack which included an iOS application, a web client and the API. During the last months I focused on the backend side as well as managing the technical team (3 people). Unfortunately, we were not able to grow as we needed to be profitable, furthermore, my cofounder and I had different ideas on how to pivot and which type of clients to pursue. I left my position in May 2015.

------