## Types of testing  


There are three types of testing:  


1. Testing under normal conditions. This is where the software application, business system or physical artefact is tested under normal working conditions and, in the case of software development, data is provided that is within the expected range.  


2. Testing under extreme conditions. This is where the software application, business system or physical artefact is subjected to conditions within the operating range but at the limits of performance expectations.  


3. Testing error behaviour. This is where the software application, business system or physical artefact is subjected to conditions outside of the performance expectations. This is where a set of tests are performed that purposefully attempts to make things go wrong, to see if things happen when they shouldn't or things don't happen when they should.  


A typical example of these processes is the testing of databases. Under normal conditions a database is interrogated using data that it is well within its limits, so if the operating limits of a field is \(0 - 99\) , then 'normal' tests would expect to receive results that are well within that range. Under extreme conditions a database is interrogated using data at the limits of a fields range, so if we take our field with the limits of \(0 - 99\) , then 'extreme' tests would expect to receive results that are 0 or 99. Finally, error tests would be carried out on our field with the limits of \(0 - 99\) , where the known results should be a negative number or a number of 100 or greater to discover how the software behaves.  


Within software development and business systems, testing is done in conjunction with the processes of 'verification' and 'validation'. It is common to see these two terms used interchangeably within industry but this is incorrect as they have the following precise definitions:  


1. Verification is the evaluation of systems, products or items with regard to conformance and consistency against pre-determined requirements. In other words "Have we built the product right?" Verification is usually checked by carrying out functional testing, which refers to activities that verify a specific action or function of software code or product or system functionality against a desired response.  


2. Validation is the process of checking the product that has been built against the specification identified or agreed with the customer. In other words "Have we built the right product?" Validation is usually checked via non-functional testing that may not be related to a specific function or user action. Non-functional requirements tend to be those that reflect the quality of the product, particularly in the context of suitability from the perspective of the customer or end users. The non-functional testing of software describes the attributes of the system as a whole. In other words how well the complete system should carry out its purpose. Below are a selection of examples of non-functional software tests:  


- Load Test: The measurement of the system behaviour for increasing system loads. For example the number of users that work simultaneously or the number of transactions. An example of this could be the testing of a client/server website, for instance to investigate the number of hits per unit of time and what kind of performance is required under such loads (such as web server response time or database query response times).  


- Performance Test: The measuring of the processing speed and response time for particular use cases, usually dependent on increasing load. What kind of performance is expected on the client side of our website (e.g how fast should pages appear, how fast should animations, applets etc. load and run)?  


- Volume Test: The observation of the system behaviour dependent on the amount of the data (e.g processing of very large files).  


- Stress Test: The observation of the system behaviour when it is overloaded.  


- Security test: The testing of security against una
