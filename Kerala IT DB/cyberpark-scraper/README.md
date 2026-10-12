+# Cyberpark Company Dataset — Authoritative Audit

## 1. Project Overview
This README consolidates the two Cyberpark company CSVs and the scraper error log in this directory. It is the primary human-readable reference for AI JobHunt; it does not assert uninspected scraper functionality.

## 2. Documentation Purpose and Scope
Only the three files in this directory were audited. No external site, API, application, database, credential, environment variable, or unrelated directory was accessed. Original CSV files were not changed. Classification is based only on stated source evidence and is not independent verification.

## 3. Source Files

| Source file | Format | Information contained | Record count | Notes |
|---|---|---|---:|---|
| `cyberpark_companies.csv` | CSV | Company name, website, Cyberpark listing URL, source URL, location | 75 | Every row says Kozhikode, Kerala. |
| `cyberpark_company_enriched.csv` | CSV | Company/contact/location details, descriptions, services, URLs, and supplied job metadata | 75 | Exact-name companion record for each base CSV company. |
| `errors.csv` | CSV | Error metadata | 1 | One `MISSING_COMPANY_NAME` skipped card; not an identifiable company. |

## 4. Executive Summary

- Files audited: 3. Total source records: 151 (150 company rows and one error row). Unique identifiable companies: 75.
- Confirmed duplicate records: 75; each name appears once in each company CSV. Possible duplicates: 0.
- Classification memberships: IT/ITeS 62; software development 51; other technology 6; non-IT/other business 5; unknown/insufficient evidence 4. Memberships may overlap.
- Missing leadership/contact value: 2 (Aufait Technologies Pvt Ltd and Platinum Ace Backend Solutions LLP).

## 5. Company Classification Methodology

IT/ITeS needs stated IT services, technology solutions, platforms, infrastructure, support, or ITeS. Software development needs explicit development, engineering, applications, products/platforms, or implementation/customization. Other technology covers stated cybersecurity, education technology, robotics, security systems, or construction technology without established software development. Non-IT reflects marketing, management, engineering-detailing, or accounting as the stated primary activity. Unknown reflects missing, contradictory, or domain-only evidence. Company names, location, and relevance scores alone are not evidence.

## 6. Consolidated Company Directory

Each entry merges the exact-name records in both company CSVs. All enriched-file fields are retained below. The base file contributes the common Kozhikode, Kerala location and duplicate source provenance. Leadership/contact values and `MD, CEO` designation fields are source-supplied only, not independently verified.

### Adam Finastra Private Limited.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Adam Finastra Private Limited
- company_name: Adam Finastra Private Limited.
- address: Unit 2E, 3rd Floor Sahya Building, Govt Cyberpark, Kozhikode, Kerala, India
- pincode: 673014
- phone: 9447370787
- email: hr@adamfinastra.tech
- website: http://www.adamfinastra.com
- contact_name: Managing Director: Muhammed Faizal Chirakkal
- designation: MD, CEO
- company_description: Adam Finastra Private Limited
- domain_expertise: Information technology consulting and support services Information technology design and development services Hosting and information technology infrastructure provisioning services Other information technology services nowhere else classified Other professional, technical and business services nowhere else classified
- cyberpark_listing_url: https://cyberparks.in/listings/adam-finastra-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: IT Consulting / IT Services
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists IT Consulting and IT Services, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in IT Consulting and IT Services and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Axel Technologies Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Axel Technologies is an established technology consultant in enterprise business solutions and focuses on providing end to end software solutions to clients to operate their business in both mobile and web platforms. The company has vast experience in designing completely customised web-based, mobile-based, distributed or stand-alone software applications, which are created specifically with the requirements of specific industries like HVAC, Logistics and Facility Management and their workflow in mind.
- company_name: Axel Technologies Pvt Ltd.
- address: 2nd Floor, Sahya Building, Cyberpark Kozhikode.
- pincode: Not available in source files.
- phone: 04952959900
- email: contact@axeltechnologies.com
- website: http://www.axeltechnologies.com
- contact_name: Afsal Nishad
- designation: MD, CEO
- company_description: Axel Technologies is an established technology consultant in enterprise business solutions and focuses on providing end to end software solutions to clients to operate their business in both mobile and web platforms. The company has vast experience in designing completely customised web-based, mobile-based, distributed or stand-alone software applications, which are created specifically with the requirements of specific industries like HVAC, Logistics and Facility Management and their workflow in mind.
- domain_expertise: Web Development, Mobile apps development, ERP management, Facilities Management, Field Service software.
- cyberpark_listing_url: https://cyberparks.in/listings/axel-technologies-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / Software Development / Enterprise Software
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and Software Development, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and Software Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### CodeAce IT Solutions LLP.
- Audit business type: Non-IT / other business
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: We are a team of creative and skilled marketing 'ninjas' with experience in search engine optimization, social media marketing and pay per click, and we are keen in High-Intent Lead Generation through our diversified advertising strategies
- company_name: CodeAce IT Solutions LLP.
- address: UNIT 4B , 2nd Floor , Sahya Building
- pincode: Not available in source files.
- phone: 9809901499
- email: admin@codeace.com
- website: https://www.codeace.com
- contact_name: Managing Director: Jijin Mohan, Sarath Kumar, Mohan Kottur
- designation: MD, CEO
- company_description: We are a team of creative and skilled marketing 'ninjas' with experience in search engine optimization, social media marketing and pay per click, and we are keen in High-Intent Lead Generation through our diversified advertising strategies
- domain_expertise: Search Engine Optimization, Search Engine Marketing, Social Media Marketing, Pay Per Click Advertising, Content Marketing, Email Marketing, ECom Marketing, Web Design and Development.
- cyberpark_listing_url: https://cyberparks.in/listings/codeace-it-solutions-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### D4 Integrated Security Solutions LLP.
- Audit business type: Other technology
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: Risk Assessment and Design Solutions
- company_name: D4 Integrated Security Solutions LLP.
- address: Unit 5A, Ground Floor, Sahya Building
- pincode: Not available in source files.
- phone: 6235336669, 6235336679
- email: info@dfoursec.com
- website: http://www.dfoursec.com
- contact_name: Siyajar Parambath
- designation: MD, CEO
- company_description: Risk Assessment and Design Solutions
- domain_expertise: Security Systems
- cyberpark_listing_url: https://cyberparks.in/listings/d4-integrated-security-solutions-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Eljo Services Private Limited.
- Audit business type: Non-IT / other business
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: Remote Business Management Services for Western Companies
- company_name: Eljo Services Private Limited.
- address: Sahya Business Centre, Cyber Park, Kozhikode
- pincode: Not available in source files.
- phone: 04952956538
- email: michael@eljoservices.com
- website: http://www.eljoservices.com
- contact_name: Shaju Jose
- designation: MD, CEO
- company_description: Remote Business Management Services for Western Companies
- domain_expertise: Management services
- cyberpark_listing_url: https://cyberparks.in/listings/eljo-services-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Freston Analytics Private Limited..
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: Freston Analytics Private Limited. Founded in 2021, Freston is a fast- growing information Technology company focusing on high end systems and solutions elevating potentials. Innovation is what we are built on. Our services and business strategy are designed to provide flexibility and choice for the customers in implementing world class solutions.
- company_name: Freston Analytics Private Limited..
- address: Sahya Building, Cyberpark
- pincode: 673014
- phone: 7025 992 051
- email: hr@frestonanalytics.in
- website: http://www.frestonanalytics.com
- contact_name: Muhammed Mukhtaar
- designation: MD, CEO
- company_description: Freston Analytics Private Limited. Founded in 2021, Freston is a fast- growing information Technology company focusing on high end systems and solutions elevating potentials. Innovation is what we are built on. Our services and business strategy are designed to provide flexibility and choice for the customers in implementing world class solutions.
- domain_expertise: Telecom, Finance, Healthcare, Education, Public Safety
- cyberpark_listing_url: https://cyberparks.in/listings/freston-analytics-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: Healthcare IT
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists Healthcare IT, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in Healthcare IT and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Gritstone Technologies LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Gritstone Technologies is a product engineering firm where we turn proof-of-concepts into market-ready products and platforms and scale them to achieve value and business goals. We leverage our extreme engineering capability to build innovative offerings in the EdTech, HeathTech and FinTech space.
- company_name: Gritstone Technologies LLP.
- address: 1st and 3rd Floor, Sahya Building
- pincode: 673014
- phone: 6238794744
- email: Hr_communications@grit-stone.com
- website: http://www.gritstonetech.com
- contact_name: Pankajakshi Maruthiat & Geetha Radhakrishnan
- designation: MD, CEO
- company_description: Gritstone Technologies is a product engineering firm where we turn proof-of-concepts into market-ready products and platforms and scale them to achieve value and business goals. We leverage our extreme engineering capability to build innovative offerings in the EdTech, HeathTech and FinTech space.
- domain_expertise: Engineering, Healthcare & Finance
- cyberpark_listing_url: https://cyberparks.in/listings/gritstone-technologies-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: FinTech / EdTech / Healthcare IT
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists FinTech and EdTech and Healthcare IT, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in FinTech and EdTech and Healthcare IT and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### IPIX TECH SERVICES PVT LTD.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: IPIX Technologies is a part of a conglomerate of companies under the umbrella of the Kreston Menon Group , a prominent business advisory firm in the UAE. With Headquarters in Dubai, and offices in various parts of the UAE, the firm has been excelling in the software development as well as digital solutions field for over a decade. The company is also focusing more into AI, Big data and upcoming other technologies.
- company_name: IPIX TECH SERVICES PVT LTD.
- address: IPIX TECH SERVICES PVT LTD KSITIL Special Economic Zone, Unit No. 03, 1st Floor, Sahya Building, Govt. Cyber Park, Nellikode (PO), Calicut, Kerala, India - 673016
- pincode: 673016
- phone: +91 9544 800 204
- email: hr@ipixtechnologies.com
- website: https://www.ipixtechnologies.com
- contact_name: Raju Menon , Unnikrishnan E M , Kavitha Gopan -, Mahmood Bangara Abdul Rahiman
- designation: MD, CEO
- company_description: IPIX Technologies is a part of a conglomerate of companies under the umbrella of the Kreston Menon Group , a prominent business advisory firm in the UAE. With Headquarters in Dubai, and offices in various parts of the UAE, the firm has been excelling in the software development as well as digital solutions field for over a decade. The company is also focusing more into AI, Big data and upcoming other technologies.
- domain_expertise: Enterprise Resource Planning, Governance Risk Management, Internal Audit Management, Learning Management System, HRMS, Time based Project Management System, Audit and Compliance software to create customized solutions to enable technology-driven sustainable growth of client's business. IPIX also provides an assortment of services in web and mobile application development together with web graphic design, user experience design, interface design, search engine optimization and related aspects of code-writing. With 3000+ clients, and an expert team of over 100+ highly qualified professionals from diverse technological and geographical backgrounds, they have made bold, giant strides in the digital world, and are a name to reckon with.
- cyberpark_listing_url: https://cyberparks.in/listings/ipix-tech-services-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / Software Development / Digital Solutions
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and Software Development and Digital Solutions, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and Software Development and Digital Solutions aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Lenok Solutions.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: Aviation software Microsoft Dynamics Business Intelligence, Microsoft PowerBI
- company_name: Lenok Solutions.
- address: Office No. 17 Cyberpark
- pincode: 673016
- phone: 04952922447
- email: mushthaq@lenoksolutions.com
- website: http://www.lenoksolutions.com
- contact_name: Shabeer Abdul Quadar
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Aviation software Microsoft Dynamics Business Intelligence, Microsoft PowerBI
- cyberpark_listing_url: https://cyberparks.in/listings/lenok-solutions/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Logiology Solutions Pvt. Ltd..
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Logiology Solutions creates custom software designed to streamline operations, boost efficiency, and drive growth across industries. Specializing in ERP, CRM, billing, and inventory solutions, we’re committed to delivering innovative technology and exceptional support, empowering businesses to achieve their goals
- company_name: Logiology Solutions Pvt. Ltd..
- address: KSITIL Special Economic Zone, 1st floor, Sahya building, Govt Cyberpark Kozhikode Nellikode (PO) Calicut, Kerala, India Pincode : 673016
- pincode: 673008
- phone: 6282683799
- email: info@logiology.com
- website: https://logiology.com/
- contact_name: Stino K James
- designation: MD, CEO
- company_description: Logiology Solutions creates custom software designed to streamline operations, boost efficiency, and drive growth across industries. Specializing in ERP, CRM, billing, and inventory solutions, we’re committed to delivering innovative technology and exceptional support, empowering businesses to achieve their goals
- domain_expertise: Enterprise Solutions, Web Design & Development, Custom Software Development, Mobile App Development, UI/UX Designing, Process Automation, Efficiency Tools, Business Software, Data Insights, Workflow Systems, Tech Empowerment
- cyberpark_listing_url: https://cyberparks.in/listings/infopeak/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / Software Development / Enterprise Software
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and Software Development and Enterprise Software, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and Software Development and Enterprise Software aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### LUZIA LAB LLP.
- Audit business type: Other technology
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: Our aim is to enhance the whole learning system by the most excited and result-oriented Technological implementation.
- company_name: LUZIA LAB LLP.
- address: Sahya Building, 3rd Floor
- pincode: Not available in source files.
- phone: 9745824596
- email: info@iluzialabs.com
- website: http://www.iluzialabs.com
- contact_name: Noufal.P (CEO)
- designation: MD, CEO
- company_description: Our aim is to enhance the whole learning system by the most excited and result-oriented Technological implementation.
- domain_expertise: Global Quality educational service
- cyberpark_listing_url: https://cyberparks.in/listings/luzia-lab-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Medaura Infotech PVT LTD.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Medaura is a healthcare technology solutions company focused on the development of integrated clinic and hospital management software. The company provides digital platforms that support clinical operations, patient records, administrative workflows, human resource management, billing, and analytics. Medaura combines healthcare domain expertise with technology-driven solutions to help healthcare providers improve operational efficiency, compliance, and quality of care.
- company_name: Medaura Infotech PVT LTD.
- address: SBC Unit-12, Upper basement, Sahya Building, Government Cyber Park
- pincode: 673014
- phone: +91 9656706444
- email: hr@medaura.io
- website: https://medaura.io/
- contact_name: SALMANUL FARIS TM
- designation: MD, CEO
- company_description: Medaura is a healthcare technology solutions company focused on the development of integrated clinic and hospital management software. The company provides digital platforms that support clinical operations, patient records, administrative workflows, human resource management, billing, and analytics. Medaura combines healthcare domain expertise with technology-driven solutions to help healthcare providers improve operational efficiency, compliance, and quality of care.
- domain_expertise: Hospitals and Health Care
- cyberpark_listing_url: https://cyberparks.in/listings/medaura-infotech-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: Healthcare IT
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists Healthcare IT, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in Healthcare IT and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### MOJGENIE IT SOLUTIONS PRIVATE LIMITED.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Worked on the following apps – Payment service provider app, Cloud (server) management application, Online teaching and training application, Webrtc based video engine, VPN solutions, VoIP.
- company_name: MOJGENIE IT SOLUTIONS PRIVATE LIMITED.
- address: Unit No. 22/B1, Sahya Building
- pincode: 673014
- phone: 8301991502
- email: info@mojgenie.com
- website: https://mojgenie.com
- contact_name: NOUFAL PANOLAN
- designation: MD, CEO
- company_description: Worked on the following apps – Payment service provider app, Cloud (server) management application, Online teaching and training application, Webrtc based video engine, VPN solutions, VoIP.
- domain_expertise: Laravel PHP, React, Veujs, React Native, Android, Swift, Objective C, Kotlin Server expertise – Container, AWS, GCP, DO, VPN, Linod
- cyberpark_listing_url: https://cyberparks.in/listings/mojgenie-it-solutions-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: Cloud/DevOps
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists Cloud/DevOps, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in Cloud/DevOps and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Pfactorial Technologies Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Pfactorial Technologies specializes in end to end AI application development, transforming business needs into intelligent solutions through custom-built models. Our core services include data and business analytics, machine and deep learning, NLP, computer vision, generative AI, and interactive data visualization. Pfactorial developed AI driven apps for real time decision making, automation, personalization, and predictive insights helping businesses unlock the power of data.
- company_name: Pfactorial Technologies Pvt Ltd.
- address: B14 , Sahya Building, CYBERPARK, Nellikode, Kozhikode, Kerala
- pincode: 673014
- phone: 9972867390
- email: hr@pfactorial.ai
- website: https://pfactorial.ai/
- contact_name: ARUN SAHADEV
- designation: MD, CEO
- company_description: Pfactorial Technologies specializes in end to end AI application development, transforming business needs into intelligent solutions through custom-built models. Our core services include data and business analytics, machine and deep learning, NLP, computer vision, generative AI, and interactive data visualization. Pfactorial developed AI driven apps for real time decision making, automation, personalization, and predictive insights helping businesses unlock the power of data.
- domain_expertise: Artificial Intelligence (AI), Machine Learning (ML), Data Science, Business Analytics, and AI Applications Development
- cyberpark_listing_url: https://cyberparks.in/listings/pfactorial-technologies-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development / AI/ML
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development and AI/ML, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development and AI/ML aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Sapling Creations Private Limited.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Sapling creations is a software product development company providing UI/UX designs, Productivity add-ons, and SaaS applications. The company was founded in November 2017 with a simple mission that business deserves a better class of software. We are a team of consultants, designers, and software engineers who understand the customer's needs and build web applications that are highly intuitive and visually stunning. Our solutions are used by clients in over 70+ countries worldwide.
- company_name: Sapling Creations Private Limited.
- address: Unit No 2c, 2nd floor, Sahya Building
- pincode: 673016
- phone: 9400903663
- email: hr@saplingcreations.com
- website: https://saplingcreations.com/
- contact_name: Anand R Krishnan
- designation: MD, CEO
- company_description: Sapling creations is a software product development company providing UI/UX designs, Productivity add-ons, and SaaS applications. The company was founded in November 2017 with a simple mission that business deserves a better class of software. We are a team of consultants, designers, and software engineers who understand the customer's needs and build web applications that are highly intuitive and visually stunning. Our solutions are used by clients in over 70+ countries worldwide.
- domain_expertise: UI/UX Design, SaaS applications, Software Development
- cyberpark_listing_url: https://cyberparks.in/listings/sapling-creations-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Software Development / SaaS / Software Product
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Software Development and SaaS, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Software Development and SaaS aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Tigabits Technologies LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Tigabits Technologies LLP is an India based leading technology service provider delivering comprehensive IT solutions for businesses across the globe. Since its inception in 2018, The Company is focused on developing E-commerce Solutions for start-ups, small and medium businesses and other enterprise level organizations. We have specialized team for Custom Software Development, Web Development, Mobile App Development, Digital Branding and other IT Outsourcing Services.
- company_name: Tigabits Technologies LLP.
- address: 3rd Floor, Unit 2K, Sahya Building
- pincode: Not available in source files.
- phone: 0495 2991811
- email: hr@tigabits.com
- website: http://www.tigabits.com
- contact_name: Muhammed Mubarek
- designation: MD, CEO
- company_description: Tigabits Technologies LLP is an India based leading technology service provider delivering comprehensive IT solutions for businesses across the globe. Since its inception in 2018, The Company is focused on developing E-commerce Solutions for start-ups, small and medium businesses and other enterprise level organizations. We have specialized team for Custom Software Development, Web Development, Mobile App Development, Digital Branding and other IT Outsourcing Services.
- domain_expertise: Ecommerce development, multi-vendor retail marketplace, on-demand delivery service marketplace, custom web and mobile app development
- cyberpark_listing_url: https://cyberparks.in/listings/tigabits-technologies-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / E-commerce / Software Development / Digital Solutions / IT Services
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and E-commerce, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and E-commerce aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### VIKN CODES.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Vikn codes is a software company with over three years of experience in the IT sector, providing services such as web development, software development and branding. We are a full service, digital agency, born to ensure the well being of your whole business. From Web and App development to ERP solution and tax auditing, we offer a full suite of marketing services. By combining people, creativity and technology, we help deliver the most innovative web solutions for businesses. No matter what service you choose. The idea behind our approach is always the same- To help you simplify the process of getting your dreams into reality.
- company_name: VIKN CODES.
- address: Office No.11, UB- Sahya
- pincode: 673016
- phone: 9577500400
- email: info@vikncodes.com
- website: http://www.vikncodes.com
- contact_name: Irshad KK Salmanul Faris Suhail K K Muhammed Shaheen K
- designation: MD, CEO
- company_description: Vikn codes is a software company with over three years of experience in the IT sector, providing services such as web development, software development and branding. We are a full service, digital agency, born to ensure the well being of your whole business. From Web and App development to ERP solution and tax auditing, we offer a full suite of marketing services. By combining people, creativity and technology, we help deliver the most innovative web solutions for businesses. No matter what service you choose. The idea behind our approach is always the same- To help you simplify the process of getting your dreams into reality.
- domain_expertise: App Development, Web designing, Graphic designing, Web development, ERP Solutions
- cyberpark_listing_url: https://cyberparks.in/listings/vikn-codes/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Software Development / Enterprise Software
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Software Development and Enterprise Software, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Software Development and Enterprise Software aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Yarddiant Weblounge Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Web development company focusing on Wordpress CMS and Learning Management System.
- company_name: Yarddiant Weblounge Pvt Ltd.
- address: Office No – 12, Sahya Building, Govt. Cyber Park, Calicut.
- pincode: Not available in source files.
- phone: +91 9895035143
- email: hr@yarddiant.com
- website: https://www.yarddiant.com
- contact_name: Prasoon Prahaladan
- designation: MD, CEO
- company_description: Web development company focusing on Wordpress CMS and Learning Management System.
- domain_expertise: Wordpress Development & Learning Management System (LMS)
- cyberpark_listing_url: https://cyberparks.in/listings/yarddiant-weblounge-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### ZOONDIA.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: ZOONDIA Established in 2008, Zoondia came about in order to fill a gap in the mobile, cloud and web applications market. Created to supply the demand for affordable and efficient development outsourcing solutions, Zoondia came about as a result of the pooling together of the top technological development talents of India. We have a large operations facility in Technopark, Trivandrum Kerala India but we also maintain offices in several parts of the US and Middle East. We take pride in our team of highly trained, committed, and talented professionals who come from a diverse set of backgrounds such as Open Source technologies computing and Java programming. Zoondia is a leading provider of technology solutions and custom software development, one who is dedicated to the development of customized, creative and affordable solutions that can meet the needs of our expanding clients. Through leveraging of our skills in the most advanced information technology, we are able to assist our clients in boosting productivity, efficiency and workflow. We consider ourselves as experts and innovators in the fields of mobile applications technology, cloud application development, custom software development, Web design architecture, Business Catalyst Development, Internet/Intranet application development, SEO building, e-Commerce, and graphic design. Our commitment to offering an exceptional experience to our clients is unmatched, delivered through a means of education and personal attention to detail. Our goal is to help our clients to enjoy the technology they use, and reap the benefits it can provide for their businesses’ profits and productivity. This level of commitment makes the Zoondia experience truly unique. These days, all too often we see IT companies offering solutions but nothing that goes beyond this basic service. Companies like these fix your software before moving on without carrying out a thorough analysis and understanding of what your company’s IT needs are. Here at Zoondia, we do things the right way. We take the time to get to know what it is you want, through understanding your business and the way it operates. This, together with our commitment to seeing your business thrive, is what sets us apart from the competition.
- company_name: ZOONDIA.
- address: 1st Floor, Sahya Building, Cyberpark, GA College
- pincode: Not available in source files.
- phone: 9995612815
- email: hr@zoondia.in
- website: https://www.zoondia.com
- contact_name: Arun Sreedharan
- designation: MD, CEO
- company_description: ZOONDIA Established in 2008, Zoondia came about in order to fill a gap in the mobile, cloud and web applications market. Created to supply the demand for affordable and efficient development outsourcing solutions, Zoondia came about as a result of the pooling together of the top technological development talents of India. We have a large operations facility in Technopark, Trivandrum Kerala India but we also maintain offices in several parts of the US and Middle East. We take pride in our team of highly trained, committed, and talented professionals who come from a diverse set of backgrounds such as Open Source technologies computing and Java programming. Zoondia is a leading provider of technology solutions and custom software development, one who is dedicated to the development of customized, creative and affordable solutions that can meet the needs of our expanding clients. Through leveraging of our skills in the most advanced information technology, we are able to assist our clients in boosting productivity, efficiency and workflow. We consider ourselves as experts and innovators in the fields of mobile applications technology, cloud application development, custom software development, Web design architecture, Business Catalyst Development, Internet/Intranet application development, SEO building, e-Commerce, and graphic design. Our commitment to offering an exceptional experience to our clients is unmatched, delivered through a means of education and personal attention to detail. Our goal is to help our clients to enjoy the technology they use, and reap the benefits it can provide for their businesses’ profits and productivity. This level of commitment makes the Zoondia experience truly unique. These days, all too often we see IT companies offering solutions but nothing that goes beyond this basic service. Companies like these fix your software before moving on without carrying out a thorough analysis and understanding of what your company’s IT needs are. Here at Zoondia, we do things the right way. We take the time to get to know what it is you want, through understanding your business and the way it operates. This, together with our commitment to seeing your business thrive, is what sets us apart from the competition.
- domain_expertise: Web Development, Analytics & Big Data ,Internet of Things ,UX / UI Design,QA & Testing Cryptocurrency and Block chain, Software Consulting ,Cloud & Infrastructure ,Machine Learning ,AR/VR
- cyberpark_listing_url: https://cyberparks.in/listings/zoondia/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / E-commerce / Software Development / AI/ML / Cloud/DevOps / IT Consulting
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and E-commerce, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and E-commerce aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### ABANA Technology Private Limited.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Software design/development, customization, implementation, maintenance, testing & benchmarking Consultancy services in the field of Information Technology Customized solution development Web-based applications
- company_name: ABANA Technology Private Limited.
- address: Office No. 10, Cyber Park, Special Economic Zone, Kozhikode
- pincode: Not available in source files.
- phone: 9496591631.
- email: Info.in@abana.com.sa
- website: http://www.abanatechnology.com
- contact_name: Abdulmajeed Saleh N. Al Suhaibani
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Software design/development, customization, implementation, maintenance, testing & benchmarking Consultancy services in the field of Information Technology Customized solution development Web-based applications
- cyberpark_listing_url: https://cyberparks.in/listings/abana-technology-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Acadeno Technologies Private Limited.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Acadeno Technologies Private Limited is a software product development division headquartered within a Special Economic Zone (SEZ), purpose-built for research, development, and innovation in modern software technologies. We partner with businesses and brands to design, build, and scale intelligent digital solutions — including the seamless integration of AI capabilities into existing software products and platforms. From enterprise-grade applications to AI-native systems, Acadeno Technologies transforms complex technology challenges into competitive advantage, empowering organizations to operate smarter, grow faster, and lead with confidence in an increasingly digital world.
- company_name: Acadeno Technologies Private Limited.
- address: Unit 19,Govt. Cyber Park, Sahya Building, Kozhikode,
- pincode: 673016
- phone: +91 4954 600 504 / +91 9895 600 504
- email: hr@acadeno.com
- website: http://www.acadeno.com
- contact_name: SRUTHI E GIREESHAN
- designation: MD, CEO
- company_description: Acadeno Technologies Private Limited is a software product development division headquartered within a Special Economic Zone (SEZ), purpose-built for research, development, and innovation in modern software technologies. We partner with businesses and brands to design, build, and scale intelligent digital solutions — including the seamless integration of AI capabilities into existing software products and platforms. From enterprise-grade applications to AI-native systems, Acadeno Technologies transforms complex technology challenges into competitive advantage, empowering organizations to operate smarter, grow faster, and lead with confidence in an increasingly digital world.
- domain_expertise: AI Solutions, RAG Knowledge Systems; Web App Development, Mobile App Development, Digital Marketing, IoT Solutions, Robotics & Automation, API & System Integration, AI Consulting & Training, Data Analytics & BI.
- cyberpark_listing_url: https://cyberparks.in/listings/acadeno-technologies-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / AI/ML / Digital Solutions / Software Product
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and AI/ML and Digital Solutions, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and AI/ML and Digital Solutions aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Analystor Technologies.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: • Application Development • CRM solutions • Analytics and Reporting • Learning Solutions • Maintenance and Support • Mobile App Development • Process Management • SharePoint Solutions
- company_name: Analystor Technologies.
- address: 3A, 3rd Floor, Sahya Building
- pincode: Not available in source files.
- phone: 495-4025055
- email: Hr_analystor@analystortech.com
- website: http://www.analystortech.com
- contact_name: Saleem Muhammed ( CEO)
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: • Application Development • CRM solutions • Analytics and Reporting • Learning Solutions • Maintenance and Support • Mobile App Development • Process Management • SharePoint Solutions
- cyberpark_listing_url: https://cyberparks.in/listings/analystor-technologies/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / Software Development
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and Software Development, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and Software Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Artifitia Solutions LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Artifitia Solutions, one of the leading web development company in Calicut, with over 20 years of industry experience, has delivered some of the best solutions on the market. Our primary goal is to continue excelling in what we do best. We recognize that every project is one-of-a-kind, so we personalize our approach to each client. From the first idea to the final launch, we collaborate closely with our clients to bring their vision to life. Using the latest tools and technologies, we develop innovative applications that exceed industry standards and shine in today's competitive market
- company_name: Artifitia Solutions LLP.
- address: Unit No. 26
- pincode: 673014
- phone: 04953501156
- email: info@artifitia.com
- website: https://www.artifitia.com/
- contact_name: Noushad CK
- designation: MD, CEO
- company_description: Artifitia Solutions, one of the leading web development company in Calicut, with over 20 years of industry experience, has delivered some of the best solutions on the market. Our primary goal is to continue excelling in what we do best. We recognize that every project is one-of-a-kind, so we personalize our approach to each client. From the first idea to the final launch, we collaborate closely with our clients to bring their vision to life. Using the latest tools and technologies, we develop innovative applications that exceed industry standards and shine in today's competitive market
- domain_expertise: MERN STACK Development, Mobile app development, WordPress development, Python Django development , Flutter development, E-commerce development, UI/UX, Web Hosting , UI/UX Design
- cyberpark_listing_url: https://cyberparks.in/listings/artifitia-solutions-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / E-commerce
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and E-commerce, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and E-commerce aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Aufait Technologies Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Aufait is an Information Technology services company providing comprehensive, user oriented Portal implementation services. Aufait's expertise in UX design, advanced Workflow/Business Process Management (BPM), Mobility, Cloud and Enterprise 2.0 has helped companies achieve significant returns on investment through strategic portal infrastructure that enable organizations leverage collective intelligence of employees. Aufait persistently aims to exceed customer expectation by focusing on value-based solutions through right consultancy and teamed talent. Since 2003, Aufait has built an enviable reputation as an expert in Web & Enterprise portals, and BPM arena. With its specialized domain specific solutions for Airline, Manufacturing and Educational industries, coupled with technology partnerships with companies such as Intalio and Microsoft, Aufait is well equipped with the competence to cater to the best in industry quality solutions with innovative products and technologies. Aufait has served customers across the globe; staying focused on long term relationship and time bound delivery of projects with budget precision. This proven track record was instrumental in earning credibility and customer loyalty with repeat business. Aufait has delivered solutions for large International customers and has a towering presence in the Middle-East.
- company_name: Aufait Technologies Pvt Ltd.
- address: SAHYA Building, CYBERPARK Kozhikode, 1st floor, Unit 4
- pincode: 673001
- phone: +91 495 4077444 , +91 495 4012221
- email: info@aufait.in
- website: http://www.aufait.in
- contact_name: Not available in source files.
- designation: Not available in source files.
- company_description: Aufait is an Information Technology services company providing comprehensive, user oriented Portal implementation services. Aufait's expertise in UX design, advanced Workflow/Business Process Management (BPM), Mobility, Cloud and Enterprise 2.0 has helped companies achieve significant returns on investment through strategic portal infrastructure that enable organizations leverage collective intelligence of employees. Aufait persistently aims to exceed customer expectation by focusing on value-based solutions through right consultancy and teamed talent. Since 2003, Aufait has built an enviable reputation as an expert in Web & Enterprise portals, and BPM arena. With its specialized domain specific solutions for Airline, Manufacturing and Educational industries, coupled with technology partnerships with companies such as Intalio and Microsoft, Aufait is well equipped with the competence to cater to the best in industry quality solutions with innovative products and technologies. Aufait has served customers across the globe; staying focused on long term relationship and time bound delivery of projects with budget precision. This proven track record was instrumental in earning credibility and customer loyalty with repeat business. Aufait has delivered solutions for large International customers and has a towering presence in the Middle-East.
- domain_expertise: Sharepoint , Liferay , Oracle Web Center , Mobility
- cyberpark_listing_url: https://cyberparks.in/listings/aufait-technologies-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: Cloud/DevOps / IT Services
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists Cloud/DevOps and IT Services, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in Cloud/DevOps and IT Services and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### BPRACT.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Bpract Software Solutions LLP “Success doesn't happen overnight!” The term 'Bpract' is the quintessence of 'being practical with best practices', and with this vision, Bpract has been growing fast ever since its inception in 2015, and within a short period of time, has attracted small to large brands, and holding a huge client base all over from the world. Bpract is a software product development company providing services for designing, development, and digital marketing services. Delivering high-quality projects to clients is our aim. And we provide the highest-caliber services to our customers. Our professional team of software engineers, designers and analysts develop and deploy applications effectively. We provide clients with quality works that are appealing and the best. Bpract Software Solutions LLP provides excellent services on a global scale and has worked with top tech companies in a range of industries. Due to our collaboration with top firms, our team has gained expertise in all levels of the IT industry. Our team gained experience from projects that were successfully completed for reputable businesses.
- company_name: BPRACT.
- address: Unit 1A, 4th floor, SAHYA
- pincode: 673016
- phone: 08129184448
- email: hr@bpract.com
- website: https://bpract.com
- contact_name: Dijil P
- designation: MD, CEO
- company_description: Bpract Software Solutions LLP “Success doesn't happen overnight!” The term 'Bpract' is the quintessence of 'being practical with best practices', and with this vision, Bpract has been growing fast ever since its inception in 2015, and within a short period of time, has attracted small to large brands, and holding a huge client base all over from the world. Bpract is a software product development company providing services for designing, development, and digital marketing services. Delivering high-quality projects to clients is our aim. And we provide the highest-caliber services to our customers. Our professional team of software engineers, designers and analysts develop and deploy applications effectively. We provide clients with quality works that are appealing and the best. Bpract Software Solutions LLP provides excellent services on a global scale and has worked with top tech companies in a range of industries. Due to our collaboration with top firms, our team has gained expertise in all levels of the IT industry. Our team gained experience from projects that were successfully completed for reputable businesses.
- domain_expertise: Laravel Application Development, Android Application Development, iOS Application Development, Web Portal and CMS Development, Custom Software Maintenance, Web and Cloud Applications, Mobile Strategy Consulting, CRM Solutions, UI/UX, Web Hosting, UI/UX Design and Enterprise Technology Automation, Search Engine Optimization, Search Engine Marketing, Social Media Marketing, Pay Per Click Advertising, Content Marketing & Email Marketing.
- cyberpark_listing_url: https://cyberparks.in/listings/bpract/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development / Cloud/DevOps / Software Product
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development and Cloud/DevOps and Software Product, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development and Cloud/DevOps and Software Product aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### CADMUS ENGINEERING SERVICES PRIVATE LIMITED.
- Audit business type: Non-IT / other business
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: CADMUS - Specialize in the field of The AEC industry consists of separate players -- Architecture, Engineering and Construction. CADMUS is an experienced Steel Detailing Company providing the excellent and reliable Steel Detailing Services in USA for commercial, industrial, residential and other related space with the focus on matching the international standards. We provide services that gives flexibility and help to match the deadlines which keeps our clients in front for their every project. Our detailers and engineers have worked on several projects, worldwide, and are committed to the client’s success and on-time delivery of the project. A combination of experienced team of project manager, skilled detailers, and latest software system is the secret of our success to the Structural Steel Industry. Specialist engineering & architectural services & solutions company servicing clients across a range of engineering & architectural segments helping improve their engineering efficiency, support their global footprint and improve their competitiveness. Leveraging technology, domain knowledge, & our robust work planning methodology to ensure an effective global delivery model for engineering services projects, we have emerged as a partner-of-choice for leading international companies. We not only deliver drawings, but also provide a professional assessment, consultancy, suggestions and the desire to improve each project. We pride ourselves in our team of highly trained individuals with years of engineering experience.
- company_name: CADMUS ENGINEERING SERVICES PRIVATE LIMITED.
- address: Unit -4 GF, SAHYA BUILDING
- pincode: Not available in source files.
- phone: 8792459575
- email: hr@cadmussteel.com
- website: http://www.cadmussteel.com
- contact_name: Mr. Sreejith Sukumaran
- designation: MD, CEO
- company_description: CADMUS - Specialize in the field of The AEC industry consists of separate players -- Architecture, Engineering and Construction. CADMUS is an experienced Steel Detailing Company providing the excellent and reliable Steel Detailing Services in USA for commercial, industrial, residential and other related space with the focus on matching the international standards. We provide services that gives flexibility and help to match the deadlines which keeps our clients in front for their every project. Our detailers and engineers have worked on several projects, worldwide, and are committed to the client’s success and on-time delivery of the project. A combination of experienced team of project manager, skilled detailers, and latest software system is the secret of our success to the Structural Steel Industry. Specialist engineering & architectural services & solutions company servicing clients across a range of engineering & architectural segments helping improve their engineering efficiency, support their global footprint and improve their competitiveness. Leveraging technology, domain knowledge, & our robust work planning methodology to ensure an effective global delivery model for engineering services projects, we have emerged as a partner-of-choice for leading international companies. We not only deliver drawings, but also provide a professional assessment, consultancy, suggestions and the desire to improve each project. We pride ourselves in our team of highly trained individuals with years of engineering experience.
- domain_expertise: Structural Steel Detailing, Engineering & Connection Design, Steel Joist & Deck Detailing, Estimating Services, Architecture Services, and Building Information Modeling
- cyberpark_listing_url: https://cyberparks.in/listings/rydberg-engineering-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Coddle Technologies Private Limited.
- Audit business type: Unknown / insufficient evidence
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: Risk Assessment and Design Solutions
- company_name: Coddle Technologies Private Limited.
- address: 1st Floor No.17, Sahya Building, Cyberpark
- pincode: Not available in source files.
- phone: 9972810600
- email: hr@coddletech.com
- website: http://www.coddletech.com
- contact_name: Jose Baby, Binu Jayara
- designation: MD, CEO
- company_description: Risk Assessment and Design Solutions
- domain_expertise: Fintech, Real estate, Gaming, Oil & Gas, E-commerce, Data Science, and IOT
- cyberpark_listing_url: https://cyberparks.in/listings/coddle-technologies-private-limited-2/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: E-commerce / FinTech
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as E-commerce and FinTech, which aligns with full-stack software development.
- email_angle: Your stated work in E-commerce and FinTech aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### CODESAP TECHNOLOGIES LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Edutech Platforms, Enterprise Solutions, DevOps, Cloud/Web Application, Mobile Application, E-Commerce
- company_name: CODESAP TECHNOLOGIES LLP.
- address: Unit10, UB, Sahya Building, Govt Cyberpark
- pincode: 673014
- phone: +91 8139001113
- email: hr@codesap.com
- website: https://codesap.com/
- contact_name: Muhammed Rashid
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Edutech Platforms, Enterprise Solutions, DevOps, Cloud/Web Application, Mobile Application, E-Commerce
- cyberpark_listing_url: https://cyberparks.in/listings/codesap-technologies-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / E-commerce / Cloud/DevOps / Enterprise Software
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and E-commerce, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and E-commerce aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Codilar Technologies Pvt.Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Custom Magento development Magento migration Magento PWA development Magento performance optimisation Omnichannel Implementation B2B Commerce Multi-Vendor Marketplace UI/UX design eCommerce SEO & Analytics Developers for hire on a contract basis
- company_name: Codilar Technologies Pvt.Ltd.
- address: SBC Unit-8, First floor Sahya
- pincode: Not available in source files.
- phone: 8884299112
- email: hr@codilar.com
- website: http://www.codilar.com
- contact_name: Mahaveer Devabalan
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Custom Magento development Magento migration Magento PWA development Magento performance optimisation Omnichannel Implementation B2B Commerce Multi-Vendor Marketplace UI/UX design eCommerce SEO & Analytics Developers for hire on a contract basis
- cyberpark_listing_url: https://cyberparks.in/listings/codilar-technologies-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: E-commerce
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as E-commerce, which aligns with full-stack software development.
- email_angle: Your stated work in E-commerce aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### CRONUS STEEL DETAILING PVT LTD.
- Audit business type: Non-IT / other business
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: Structural Steel Detailing
- company_name: CRONUS STEEL DETAILING PVT LTD.
- address: UB-18 SAHYA BUILDINGS, CYBERPARK
- pincode: 673014
- phone: 9538819097
- email: hrd@cronussteel.com
- website: http://www.cronussteel.com
- contact_name: Mr. Vinayadas P Vijayan and Mr. Jayaghosh V Rajendran
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Structural Steel Detailing
- cyberpark_listing_url: https://cyberparks.in/listings/cronus-steel-detailing-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Dezen Consultants International Pvt Ltd.
- Audit business type: Unknown / insufficient evidence
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: 
- company_name: Dezen Consultants International Pvt Ltd.
- address: Sahya
- pincode: 673014
- phone: 6282667955
- email: admin@dezen.in
- website: http://www.dezen.in
- contact_name: Shaju Ramachandra Kurup, Ashkarali Manguzhiyil, Akhil Suresh S
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Not available in source files.
- cyberpark_listing_url: https://cyberparks.in/listings/dezen-consultants-international-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: partial
- notes: Listing has contact detail but no company description or domain expertise.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Doctosmart.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: Healthcare Management Software Firm
- company_name: Doctosmart.
- address: 2J Third Floor, Sahya Building
- pincode: Not available in source files.
- phone: 8547467231
- email: doctosmart@gmail.com
- website: http://www.doctosmart.com
- contact_name: Charls Vinod Kumar,Bijeesh Raghavan,Pratheesh M
- designation: MD, CEO
- company_description: Healthcare Management Software Firm
- domain_expertise: Clinic & Hospital Management Software
- cyberpark_listing_url: https://cyberparks.in/listings/healthcare-management-software-firm/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: Healthcare IT
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists Healthcare IT, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in Healthcare IT and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### EDUMPUS PORTAL LLP.
- Audit business type: Unknown / insufficient evidence
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: 
- company_name: EDUMPUS PORTAL LLP.
- address: 4th Unit-2, Floor Sahya
- pincode: 673009
- phone: 8714600294
- email: hr@edumpus.com
- website: http://www.edumpus.com
- contact_name: Ajesh Raj K
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Not available in source files.
- cyberpark_listing_url: https://cyberparks.in/listings/edumpus-portal-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: partial
- notes: Listing has contact detail but no company description or domain expertise.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### ERE BUSINESS SOLUTIONS PV LTD.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: EBS Supported by a team of professionals including IT experts and business experts are available as consultant for customer requirements. We can help customer to make the right decisions and create a plan that is right for business. EBS have a wide range of specialized products available in all business vertical.
- company_name: ERE BUSINESS SOLUTIONS PV LTD.
- address: Unit 2D, 2nd Floor, Sahya Bldg
- pincode: Not available in source files.
- phone: 7356568444
- email: hr@erebsindia.com
- website: http://www.erebsindia.com
- contact_name: Jiss Anto
- designation: MD, CEO
- company_description: EBS Supported by a team of professionals including IT experts and business experts are available as consultant for customer requirements. We can help customer to make the right decisions and create a plan that is right for business. EBS have a wide range of specialized products available in all business vertical.
- domain_expertise: We are in SAAS APPLICATIONS, which include specialized business Applications, Custom development, web applications, business consulting etc.
- cyberpark_listing_url: https://cyberparks.in/listings/ere-business-solutions-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / SaaS
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and SaaS, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and SaaS aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### eSynergy Technologies Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: eSynergy Technologies Pvt Ltd From online school platforms - to AI-powered online design tools - to online content-sharing platforms & much more, we're committed to making your online experience as simple as possible, bringing together deep industry expertise and the latest IT advancements to deliver products that perfectly fit the needs and behavior of users. Being a trusted software development company in India, we employ industry’s best methodologies to deliver secure, robust, and scalable software for diversified domains
- company_name: eSynergy Technologies Pvt Ltd.
- address: 4th floor, Sahya Building, Govt Cyberpark
- pincode: 673016
- phone: Not available in source files.
- email: hr@esynergysoft.com
- website: https://www.esynergysoft.com/
- contact_name: Romal Bachu Vallil
- designation: MD, CEO
- company_description: eSynergy Technologies Pvt Ltd From online school platforms - to AI-powered online design tools - to online content-sharing platforms & much more, we're committed to making your online experience as simple as possible, bringing together deep industry expertise and the latest IT advancements to deliver products that perfectly fit the needs and behavior of users. Being a trusted software development company in India, we employ industry’s best methodologies to deliver secure, robust, and scalable software for diversified domains
- domain_expertise: Online Course Creation & Selling Platforms, Learning Management System, Online Conversion SDK’s, Presentation Sharing Platforms
- cyberpark_listing_url: https://cyberparks.in/listings/esynergy-technologies-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development / AI/ML
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development and AI/ML, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development and AI/ML aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Fantacode Private Limited.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Fantacode is a premier product development studio with SAAS products in customer experience and e-commerce domain. Fantacode also empowers customers to craft custom-tailored solutions with the in house talents of experienced engineers handling all aspects of DevOps.
- company_name: Fantacode Private Limited.
- address: Unit 2F, Sahya Building, Cyberpark
- pincode: Not available in source files.
- phone: 0495-2965798
- email: hr@fantacode.com
- website: http://www.fantacode.com
- contact_name: Abdul Muhaymin
- designation: MD, CEO
- company_description: Fantacode is a premier product development studio with SAAS products in customer experience and e-commerce domain. Fantacode also empowers customers to craft custom-tailored solutions with the in house talents of experienced engineers handling all aspects of DevOps.
- domain_expertise: Enterprise SAAS in Customer Experience and Ecommerce SAAS
- cyberpark_listing_url: https://cyberparks.in/listings/fantacode-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: E-commerce / SaaS / Cloud/DevOps / Software Product
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as E-commerce and SaaS and Cloud/DevOps, which aligns with full-stack software development.
- email_angle: Your stated work in E-commerce and SaaS and Cloud/DevOps aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### GETLEAD ANALYTICS PVT LTD.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: GetLead helps Small and Medium businesses to automate their sales & marketing process by providing intuitive tools and makes their client communication simple and effective . Our Powerful CRM , SMS , Whatsapp , Voice , IVR and Ticketing tools helps businesses to achieve their Success Goals
- company_name: GETLEAD ANALYTICS PVT LTD.
- address: Not available in source files.
- pincode: Not available in source files.
- phone: +916282900762
- email: hr@getlead.co.uk
- website: http://www.getlead.co.uk
- contact_name: Akhilkrishna T
- designation: MD, CEO
- company_description: GetLead helps Small and Medium businesses to automate their sales & marketing process by providing intuitive tools and makes their client communication simple and effective . Our Powerful CRM , SMS , Whatsapp , Voice , IVR and Ticketing tools helps businesses to achieve their Success Goals
- domain_expertise: CRM, Marketing Automation , Voice Calls , IVR , SMS , Whatsapp,Digital Scratch Card
- cyberpark_listing_url: https://cyberparks.in/listings/getlead-analytics-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### GJ Global IT Ventures.
- Audit business type: Unknown / insufficient evidence
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: FinTech, EdTech, ERP Software’s, Ecommerce
- company_name: GJ Global IT Ventures.
- address: Unit 31, Sahya Building
- pincode: Not available in source files.
- phone: 8075727348
- email: hr@gjglobalsoft.com
- website: http://www.gjglobalsoft.com
- contact_name: Janakiraman R
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: FinTech, EdTech, ERP Software’s, Ecommerce
- cyberpark_listing_url: https://cyberparks.in/listings/gj-global-it-ventures/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: E-commerce / FinTech / EdTech / Enterprise Software
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as E-commerce and FinTech and EdTech, which aligns with full-stack software development.
- email_angle: Your stated work in E-commerce and FinTech and EdTech aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Globit Business Solutions Private Limited.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: A Professional Service company specialized in innovative IT Infrastructure Solutions.
- company_name: Globit Business Solutions Private Limited.
- address: Unit-2G, Sahya Building
- pincode: Not available in source files.
- phone: +91 495 296 9768
- email: calicut@gbsits.com
- website: https://gbsits.com/
- contact_name: Hasna P K
- designation: MD, CEO
- company_description: A Professional Service company specialized in innovative IT Infrastructure Solutions.
- domain_expertise: Remote Infrastructure Management Services -IT Consulting Services -Professional Service for IT Infrastructure Solutions -Cyber Security Solutions and Services -IT Vendor and Contract Management -IT Project Management Services -IT Logistic Management Services
- cyberpark_listing_url: https://cyberparks.in/listings/rims-technologies-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: Cybersecurity / IT Consulting
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists Cybersecurity and IT Consulting, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in Cybersecurity and IT Consulting and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Infinite Open Source Solutions LLP ™.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Infinite Open Source Solutions is a globally recognized software development company headquartered at Govt Cyber Park in Kozhikode, delivering innovative digital transformation solutions for businesses worldwide. With over 17+ years of industry expertise and a strong presence through 7 international offices, iOSS has established itself as one of the fastest-growing IT companies in Kerala and a trusted technology partner for startups, enterprises, and global organizations. Operating from the KSITIL Special Economic Zone at Govt Cyber Park, iOSS specializes in developing scalable, future-ready, and customized software solutions aligned to modern business needs. The company is widely recognized among the best software development companies in India and worldwide for its expertise in AI development, blockchain development, SaaS application development, custom software development, website development, and mobile application development. Since its inception in 2009, iOSS has successfully delivered technology solutions to more than 5000+ clients across multiple industries globally. The company combines technical excellence, strategic business insight, and strong project management capabilities to build high-performing digital products that drive operational efficiency, digital growth, and business success. With a dedicated team of experienced software engineers, technology consultants, SEO experts, UI/UX specialists, and business professionals, iOSS focuses on delivering secure, scalable, and innovative IT solutions aligned with evolving global market trends. Its expertise spans enterprise software development, cloud-based platforms, AI-powered business applications, blockchain ecosystems, SaaS products, eCommerce platforms, and advanced mobile technologies. What distinguishes iOSS in the global IT industry is its strong commitment to integrity, transparency, innovation, and long-term client relationships. By maintaining high standards in software engineering, digital strategy, and customer support, the company has earned a reputation as a reliable technology partner for ambitious startups, SMEs, and large international enterprises. The organization continues to expand its global footprint while delivering advanced, future-driven digital solutions to businesses around the world.
- company_name: Infinite Open Source Solutions LLP ™.
- address: KSITIL Special Economic Zone, Unit No. 03, 2nd Floor, Sahya Building, Govt Cyber Park, Kozhikode, Kerala, India
- pincode: Not available in source files.
- phone: 9544971055
- email: hr@ioss.in
- website: http://ioss.co
- contact_name: Abdul Gafoor K V, Abdul Majeed P K, Ameen Islahi, Ashok KS, Pavanan Ghosh
- designation: MD, CEO
- company_description: Infinite Open Source Solutions is a globally recognized software development company headquartered at Govt Cyber Park in Kozhikode, delivering innovative digital transformation solutions for businesses worldwide. With over 17+ years of industry expertise and a strong presence through 7 international offices, iOSS has established itself as one of the fastest-growing IT companies in Kerala and a trusted technology partner for startups, enterprises, and global organizations. Operating from the KSITIL Special Economic Zone at Govt Cyber Park, iOSS specializes in developing scalable, future-ready, and customized software solutions aligned to modern business needs. The company is widely recognized among the best software development companies in India and worldwide for its expertise in AI development, blockchain development, SaaS application development, custom software development, website development, and mobile application development. Since its inception in 2009, iOSS has successfully delivered technology solutions to more than 5000+ clients across multiple industries globally. The company combines technical excellence, strategic business insight, and strong project management capabilities to build high-performing digital products that drive operational efficiency, digital growth, and business success. With a dedicated team of experienced software engineers, technology consultants, SEO experts, UI/UX specialists, and business professionals, iOSS focuses on delivering secure, scalable, and innovative IT solutions aligned with evolving global market trends. Its expertise spans enterprise software development, cloud-based platforms, AI-powered business applications, blockchain ecosystems, SaaS products, eCommerce platforms, and advanced mobile technologies. What distinguishes iOSS in the global IT industry is its strong commitment to integrity, transparency, innovation, and long-term client relationships. By maintaining high standards in software engineering, digital strategy, and customer support, the company has earned a reputation as a reliable technology partner for ambitious startups, SMEs, and large international enterprises. The organization continues to expand its global footprint while delivering advanced, future-driven digital solutions to businesses around the world.
- domain_expertise: AI Development – Intelligent AI-powered business solutions. Blockchain Development – Secure and scalable blockchain software solutions. Custom Software Development – Custom-made software for unique business needs. SaaS Development – Cloud-based and scalable SaaS platforms. Website Development – Responsive and SEO-friendly websites. Mobile Application Development – Advanced Android and iOS applications.
- cyberpark_listing_url: https://cyberparks.in/listings/ios/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / E-commerce / Software Development / SaaS / AI/ML / Cloud/DevOps / Enterprise Software / Digital Solutions
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and E-commerce and Software Development, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and E-commerce and Software Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### IOCOD INFOTECH PVT LTD.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: IOCOD is a combination of creative and youthful team members bringing out their unique ideas in the project solutions custom-moulded according to different clients. We welcome the power of change to create 360° value for our clients, people and communities by providing cutting edge services. Our success lies in bringing customer focus and simplicity to over-complicated financial markets. With a mission to diligently deliver on the promise of technology and human ingenuity, our vision is to introduce state of the art Fintech products that exceed expectations and deliver positive outcomes for our customers. We create cutting edge solutions for your Businesses using the most modern technologies. Our culture of innovation and service means we stay focused on delivering leading solutions.
- company_name: IOCOD INFOTECH PVT LTD.
- address: Ground Floor, Sahya Building
- pincode: Not available in source files.
- phone: 9847153096
- email: info@iocod.com
- website: https://iocod.com/
- contact_name: Fasil KK
- designation: MD, CEO
- company_description: IOCOD is a combination of creative and youthful team members bringing out their unique ideas in the project solutions custom-moulded according to different clients. We welcome the power of change to create 360° value for our clients, people and communities by providing cutting edge services. Our success lies in bringing customer focus and simplicity to over-complicated financial markets. With a mission to diligently deliver on the promise of technology and human ingenuity, our vision is to introduce state of the art Fintech products that exceed expectations and deliver positive outcomes for our customers. We create cutting edge solutions for your Businesses using the most modern technologies. Our culture of innovation and service means we stay focused on delivering leading solutions.
- domain_expertise: Fintech , CRM & Laravel Based Applications
- cyberpark_listing_url: https://cyberparks.in/listings/iocod-infotech-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: FinTech
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists FinTech, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in FinTech and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### ioNob Innovations LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: At ioNob Innovations LLP, we specialize in delivering industry-focused ERP solutions designed to streamline operations and boost efficiency. With proven expertise in the manpower supply and trading sectors, our ERP platforms are built to solve real-world challenges through automation, accuracy, and scalability. ERP for Manpower Supply :- Our manpower supply ERP system empowers organizations to manage their workforce with ease. From client & manual timesheet management to project and site monitoring, we provide complete visibility into operations. Features like designation and employee mobilization tracking, flexible official/raw/missing timesheet workflows, and automated billing & invoicing ensure seamless HR and financial management. ERP for Trading Industry :- For businesses in the trading sector,ioNob Innovations LLP offers ERP solutions that enhance inventory and stock control, simplify purchase & sales workflows, and strengthen client/vendor relationship management. Integrated modules cover the entire business cycle, including quotation, order, and delivery tracking, enabling smarter decision-making and faster turnaround times.
- company_name: ioNob Innovations LLP.
- address: Unit 1A, Second Floor, Sahaya Building Govt. Cyber Park
- pincode: 673016
- phone: 8714094648
- email: hr@ionob.com
- website: https://ionob.com
- contact_name: Mujthaba P
- designation: MD, CEO
- company_description: At ioNob Innovations LLP, we specialize in delivering industry-focused ERP solutions designed to streamline operations and boost efficiency. With proven expertise in the manpower supply and trading sectors, our ERP platforms are built to solve real-world challenges through automation, accuracy, and scalability. ERP for Manpower Supply :- Our manpower supply ERP system empowers organizations to manage their workforce with ease. From client & manual timesheet management to project and site monitoring, we provide complete visibility into operations. Features like designation and employee mobilization tracking, flexible official/raw/missing timesheet workflows, and automated billing & invoicing ensure seamless HR and financial management. ERP for Trading Industry :- For businesses in the trading sector,ioNob Innovations LLP offers ERP solutions that enhance inventory and stock control, simplify purchase & sales workflows, and strengthen client/vendor relationship management. Integrated modules cover the entire business cycle, including quotation, order, and delivery tracking, enabling smarter decision-making and faster turnaround times.
- domain_expertise: Website Development & Hosting – Scalable, secure, and responsive websites that represent your brand. Digital Marketing – SEO, social media management, and online advertising to maximize visibility and lead generation. E-commerce Development – Customized e-commerce platforms to drive online sales and customer engagement. Cloud-based Software Deployment – Fast, secure, and flexible cloud solutions to ensure business continuity and scalability.
- cyberpark_listing_url: https://cyberparks.in/listings/ionob-innovations-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: E-commerce / Cloud/DevOps / Enterprise Software
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as E-commerce and Cloud/DevOps and Enterprise Software, which aligns with full-stack software development.
- email_angle: Your stated work in E-commerce and Cloud/DevOps and Enterprise Software aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### John & Smith Solutions Private Limited.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: John & Smith Solutions Private Limited is the best choice for Computing and Information Technology Services, Consultancy and Development for Healthcare and Recruitment Agencies.We have varying products and Services depending on the size of your organisation.
- company_name: John & Smith Solutions Private Limited.
- address: Govt. Cyberpark Calicut, Kerala, 673 016
- pincode: Not available in source files.
- phone: +916282802686
- email: hr@johnandsmithglobal.com
- website: http://johnandsmithglobal.com
- contact_name: Dr Jobi Chacko
- designation: MD, CEO
- company_description: John & Smith Solutions Private Limited is the best choice for Computing and Information Technology Services, Consultancy and Development for Healthcare and Recruitment Agencies.We have varying products and Services depending on the size of your organisation.
- domain_expertise: John and Smith Solutions develops innovative software products for enterprises all over the world. Our core strength has always been finding key solutions to perennial industry problems through innovative and sustained research and development, thus separating John and Smith from its competitors.
- cyberpark_listing_url: https://cyberparks.in/listings/john-smith-solutions-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Healthcare IT / IT Services / Software Product
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Healthcare IT and IT Services and Software Product, which aligns with full-stack software development.
- email_angle: Your stated work in Healthcare IT and IT Services and Software Product aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Keype Systems Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Healthcare Informatics, ERP Applications, Open Source Consulting, Data Centers & Infrastructure, Software Development.
- company_name: Keype Systems Pvt Ltd.
- address: Not available in source files.
- pincode: Not available in source files.
- phone: 7356771773
- email: career@keype.com
- website: http://www.keype.com
- contact_name: Firdous Amir
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Healthcare Informatics, ERP Applications, Open Source Consulting, Data Centers & Infrastructure, Software Development.
- cyberpark_listing_url: https://cyberparks.in/listings/keype-systems-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development / Healthcare IT / Enterprise Software
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development and Healthcare IT and Enterprise Software, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development and Healthcare IT and Enterprise Software aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### LeEYE-T Techno Hub LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Driving Business Success through Innovative Technology Solutions: LeEYET Techno Hub In today's rapidly evolving business landscape, harnessing the power of technology is essential for organizations aiming to stay ahead of the competition. Enter LeEYET Techno Hub, a leading technology company committed to empowering businesses through innovative solutions and unparalleled expertise. With a rich history rooted in over 16 years of experience in hardware, networking, hosting, server technology, software development, and management, LeEYET Techno Hub has become a trusted partner for businesses across industries. The company's founder, Mr. Shafeeque Parakulath, envisioned a future where businesses could leverage cutting-edge technologies to drive growth, efficiency, and success. What sets LeEYET Techno Hub apart is its unwavering commitment to customer satisfaction. The company's team of skilled professionals possesses deep industry knowledge and expertise in cloud computing, artificial intelligence, internet of things, and blockchain technology. This allows LeEYET Techno Hub to create tailored solutions that address the unique challenges faced by its clients. Whether it's web and mobile development, software solutions, e-commerce platforms, or digital marketing strategies, LeEYET Techno Hub offers a comprehensive suite of services to transform businesses. By partnering with LeEYET Techno Hub, organizations can unlock new opportunities, streamline operations, enhance customer experiences, and drive revenue growth. With a collaborative approach, transparent communication, and a focus on building strong partnerships, LeEYET Techno Hub goes above and beyond to understand the goals and aspirations of its clients. This customer-centric approach has garnered the trust and loyalty of businesses across the globe. Embrace the digital revolution and experience the LeEYET Techno Hub difference. Together, we will shape a future where your business thrives in the digital world.
- company_name: LeEYE-T Techno Hub LLP.
- address: Second Floor, Unit-1I, Sahya Building
- pincode: Not available in source files.
- phone: 8606644255
- email: hr@leeyet.com
- website: http://www.leeyet.com
- contact_name: Shafeeque Parakulath
- designation: MD, CEO
- company_description: Driving Business Success through Innovative Technology Solutions: LeEYET Techno Hub In today's rapidly evolving business landscape, harnessing the power of technology is essential for organizations aiming to stay ahead of the competition. Enter LeEYET Techno Hub, a leading technology company committed to empowering businesses through innovative solutions and unparalleled expertise. With a rich history rooted in over 16 years of experience in hardware, networking, hosting, server technology, software development, and management, LeEYET Techno Hub has become a trusted partner for businesses across industries. The company's founder, Mr. Shafeeque Parakulath, envisioned a future where businesses could leverage cutting-edge technologies to drive growth, efficiency, and success. What sets LeEYET Techno Hub apart is its unwavering commitment to customer satisfaction. The company's team of skilled professionals possesses deep industry knowledge and expertise in cloud computing, artificial intelligence, internet of things, and blockchain technology. This allows LeEYET Techno Hub to create tailored solutions that address the unique challenges faced by its clients. Whether it's web and mobile development, software solutions, e-commerce platforms, or digital marketing strategies, LeEYET Techno Hub offers a comprehensive suite of services to transform businesses. By partnering with LeEYET Techno Hub, organizations can unlock new opportunities, streamline operations, enhance customer experiences, and drive revenue growth. With a collaborative approach, transparent communication, and a focus on building strong partnerships, LeEYET Techno Hub goes above and beyond to understand the goals and aspirations of its clients. This customer-centric approach has garnered the trust and loyalty of businesses across the globe. Embrace the digital revolution and experience the LeEYET Techno Hub difference. Together, we will shape a future where your business thrives in the digital world.
- domain_expertise: Data Engineering, Hosting and Software Development
- cyberpark_listing_url: https://cyberparks.in/listings/leeye-t-techno-hub-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / E-commerce / Software Development / AI/ML / Cloud/DevOps
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and E-commerce and Software Development, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and E-commerce and Software Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Lilac Infotech Pvt. Ltd..
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Lilac Infotech Pvt.Ltd. started as a team of two passionate young individuals on 20th September 2018 to create engaging experiences that turn our clients into trailblazers, traffic into customers, and goals into measurable fruition outcomes. Being the tech specialists, we create solutions that allow you to do it all easily and seamlessly. Our objective is to deliver high-value solutions that drive your business forward no matter where you are in your digital journey. As an emerging startup firm, Lilac Infotech Pvt.Ltd. is resolved to contribute quality IT solutions and services around the globe by uniting both advanced technology and proven talent in a cost-efficient manner. In view of an imaginative, astute methodology we plan to incorporate the advances and business procedures to meet the necessities. Focused on delivering Product Engineering Services and technology-driven Business Solutions, Lilac has partnered with leading technology providers in diverse areas and leverages our client’s domain expertise to improve and fortify our contributions. Lilac team strives to bring people and brands closer in refreshing and exciting ways. Our Innovation and Expertise are into App Development, Web Development, Quality Assurance, Digital Marketing, Enterprise Resource Planning and Data analytics. Rely on us to help you turn data into insights quicker, streamline your infrastructure faster, advance the application experience and get control of every attributes that touches your organization. Mission Endured customer contentment with inventive design and development to convey outstanding technology infrastructure, services, and solutions that advertise characterizing astounding arrangements that make esteem and solid upper hand for our consumers around the globe. Vision To implement an environment that demeanor IT Abundance wherein the services are ingenious and swank web development and software solutions in an impending era of technology.
- company_name: Lilac Infotech Pvt. Ltd..
- address: 2nd Floor, Sahya Building, Govt. Cyberpark
- pincode: Not available in source files.
- phone: 9072982588
- email: hr@lilacinfotech.com
- website: https://www.lilacinfotech.com/
- contact_name: Muhammed Shafi PU
- designation: MD, CEO
- company_description: Lilac Infotech Pvt.Ltd. started as a team of two passionate young individuals on 20th September 2018 to create engaging experiences that turn our clients into trailblazers, traffic into customers, and goals into measurable fruition outcomes. Being the tech specialists, we create solutions that allow you to do it all easily and seamlessly. Our objective is to deliver high-value solutions that drive your business forward no matter where you are in your digital journey. As an emerging startup firm, Lilac Infotech Pvt.Ltd. is resolved to contribute quality IT solutions and services around the globe by uniting both advanced technology and proven talent in a cost-efficient manner. In view of an imaginative, astute methodology we plan to incorporate the advances and business procedures to meet the necessities. Focused on delivering Product Engineering Services and technology-driven Business Solutions, Lilac has partnered with leading technology providers in diverse areas and leverages our client’s domain expertise to improve and fortify our contributions. Lilac team strives to bring people and brands closer in refreshing and exciting ways. Our Innovation and Expertise are into App Development, Web Development, Quality Assurance, Digital Marketing, Enterprise Resource Planning and Data analytics. Rely on us to help you turn data into insights quicker, streamline your infrastructure faster, advance the application experience and get control of every attributes that touches your organization. Mission Endured customer contentment with inventive design and development to convey outstanding technology infrastructure, services, and solutions that advertise characterizing astounding arrangements that make esteem and solid upper hand for our consumers around the globe. Vision To implement an environment that demeanor IT Abundance wherein the services are ingenious and swank web development and software solutions in an impending era of technology.
- domain_expertise: Laravel Application Development, Android Application Development, iOS Application Development, Web Portal and CMS Development, Data Analytics, Quality Assurance on Software Verticals, Digital Marketing, ERP Solutions , Desktop Application , Custom Software Maintenance, Web and Cloud Applications, Mobile Strategy Consulting, CRM Solutions, UI/UX, Web Hosting , Email Services, Content Marketing, UI/UX Design and Enterprise Technology Automation
- cyberpark_listing_url: https://cyberparks.in/listings/lilac-infotech-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Software Development / Cloud/DevOps / Enterprise Software
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Software Development and Cloud/DevOps, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Software Development and Cloud/DevOps aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Limenzy Technologies Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Limenzy Technologies is a leading software development company in India providing services in IT such as outsourcing of Web Development,Web Designing & Windows Application Development.We have been serving more than hundred clients in and outside India since 2008 .We are grounded in Calicut with two branches creating global online brands with many employees.Over the years, we have developed deep expertise of mastering skills and working hand-in-hand with clients to maximize the investment in their online business efforts.
- company_name: Limenzy Technologies Pvt Ltd.
- address: Basement Floor, Sahya Building, Govt CyberPark, KSITIL SEZ, Nellikode PO, Kozhikode, Kerala, INDIA
- pincode: 673 016
- phone: +91 495 2600550
- email: anjana@limenzy.com
- website: http://www.limenzy.com
- contact_name: Vipin Anand V P
- designation: MD, CEO
- company_description: Limenzy Technologies is a leading software development company in India providing services in IT such as outsourcing of Web Development,Web Designing & Windows Application Development.We have been serving more than hundred clients in and outside India since 2008 .We are grounded in Calicut with two branches creating global online brands with many employees.Over the years, we have developed deep expertise of mastering skills and working hand-in-hand with clients to maximize the investment in their online business efforts.
- domain_expertise: PHP, IoT, Blockchain, IOS, Android, Open Source, Cloud, Big Data, Machine Learning
- cyberpark_listing_url: https://cyberparks.in/listings/limenzy-technologies-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Software Development / AI/ML / Cloud/DevOps
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Software Development and AI/ML, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Software Development and AI/ML aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Lithos Technosoft Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Lithos Technosoft Pvt Ltd Lithos Technosoft is a Retail SAAS company with more than 10 years of experience in the retail Tech space, specializing in Fintech, Point Of Sale & ERP Solutions, Application development, and IT Consultancy. We are committed to providing state-of-the-art solutions to ever-evolving retail businesses. Lithos Technosoft continues to evolve finding cutting-edge solutions to maximize ease of use stability security and efficiency.
- company_name: Lithos Technosoft Pvt Ltd.
- address: UB1, Sahya Building, Govt Cyberpark
- pincode: 673016
- phone: +91 495 3500 202
- email: hr@lithostechnosoft.com
- website: https://www.lithostechnosoft.com
- contact_name: Mohamed Jafar,Vinaya Chandran, Fahad CK
- designation: MD, CEO
- company_description: Lithos Technosoft Pvt Ltd Lithos Technosoft is a Retail SAAS company with more than 10 years of experience in the retail Tech space, specializing in Fintech, Point Of Sale & ERP Solutions, Application development, and IT Consultancy. We are committed to providing state-of-the-art solutions to ever-evolving retail businesses. Lithos Technosoft continues to evolve finding cutting-edge solutions to maximize ease of use stability security and efficiency.
- domain_expertise: SAAS, Retail Tech, Analytics, Fintech
- cyberpark_listing_url: https://cyberparks.in/listings/lithos-technosoft-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development / SaaS / FinTech / Enterprise Software
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development and SaaS and FinTech, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development and SaaS and FinTech aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Logiqdreams LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: We are an innovative technology company with interests in new technology design and development. Our core focus is to understand the client challenges and develop transformational technology that will enhance their business operations and also help to them to remain agile and lean.
- company_name: Logiqdreams LLP.
- address: 2nd Floor, Sahya Building, Cyberpark
- pincode: 673014
- phone: 9037383816
- email: hr@logiqdreams.com
- website: http://www.logiqdreams.com
- contact_name: Muralidharan VC
- designation: MD, CEO
- company_description: We are an innovative technology company with interests in new technology design and development. Our core focus is to understand the client challenges and develop transformational technology that will enhance their business operations and also help to them to remain agile and lean.
- domain_expertise: Software Development, Embedded Development, Hardware Design & Development and Animation.
- cyberpark_listing_url: https://cyberparks.in/listings/logiqdreams-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Loudchilli.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Loudchilli is a full-fledged IT Solutions and Digital Agency with a proven track record of providing premium bespoke technology solutions to help businesses embark on a journey of exceptional business growth and improved client satisfaction. Our area of expertise lies in providing our clients with top-notch digital requisites to help them launch, sustain and grow their business free of anxieties. Our exquisite range of services includes Web Services, Website Design, Enterprise Solutions, Mobile Application Development, Digital Marketing, Content Marketing, Social Media Marketing, and many more. Being the one-stop solution for all your digital needs, our services are tailor-made to meet the unique demands of our beloved clients.
- company_name: Loudchilli.
- address: Unit I B/68, 4th floor
- pincode: Not available in source files.
- phone: Not available in source files.
- email: hr@loudchilli.com
- website: http://www.loudchilli.com
- contact_name: Masoud Mohamed (CEO)
- designation: MD, CEO
- company_description: Loudchilli is a full-fledged IT Solutions and Digital Agency with a proven track record of providing premium bespoke technology solutions to help businesses embark on a journey of exceptional business growth and improved client satisfaction. Our area of expertise lies in providing our clients with top-notch digital requisites to help them launch, sustain and grow their business free of anxieties. Our exquisite range of services includes Web Services, Website Design, Enterprise Solutions, Mobile Application Development, Digital Marketing, Content Marketing, Social Media Marketing, and many more. Being the one-stop solution for all your digital needs, our services are tailor-made to meet the unique demands of our beloved clients.
- domain_expertise: Web Services, Website Design, Enterprise Solutions, Mobile Application Development, Digital Marketing, Content Marketing, Social Media Marketing, and many more.
- cyberpark_listing_url: https://cyberparks.in/listings/hexwhale-interactive-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / Software Development / Enterprise Software
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and Software Development and Enterprise Software, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and Software Development and Enterprise Software aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### LRG INTERNATIONAL PRIVATE LIMITED.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: IT Strategies, IT Project Management, IT Audit, Software Testing ,Network Management
- company_name: LRG INTERNATIONAL PRIVATE LIMITED.
- address: Unit15, UB, Sahya Building Govt CyberPark
- pincode: 673014
- phone: +91 9778698412
- email: hr.ind@lulurayyangroup.com
- website: https://lrg.international
- contact_name: MUTHUVATTUSSERRY KHALID
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: IT Strategies, IT Project Management, IT Audit, Software Testing ,Network Management
- cyberpark_listing_url: https://cyberparks.in/listings/lulurayyan-international-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### M/S INTERNATIONAL TXG PRIVATE LIMITED.
- Audit business type: Other technology
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: M/S INTERNATIONAL TXG PRIVATE LIMITED Technical Xperts Group is an international technology resource provider with the strength of technical expertise and 10 years of experience. Technical Xperts Group (TXG) is a venture of experts in the field of engineering, design, communication and management who has created histories in building world’s best and renowned landmarks. TXG’s industry-leading collaboration that delivers human resource support, training, technical project design, consultation and support for VDC, global engineering, CAD services and coordinated BIM modelling. TXG is committed to deliver solutions and services for leading companies across the world. Our values and professionalism in creating world class support has its own benchmark. Our comprehensive and collaborated support increases efficiency and sustainability, improve operational performance, maximize profit value, and ensure seamless incorporation of future technologies. TXG support customer growth through our customized solutions and strategies, which help us to deliver commitments. The expertise of our team, along with a strong network, is the key to our success.
- company_name: M/S INTERNATIONAL TXG PRIVATE LIMITED.
- address: Unit No:6, GF, Sahya building, Government cyberpark
- pincode: Not available in source files.
- phone: +91 87147 79951
- email: info@txglive.com
- website: https://www.txglive.com
- contact_name: Managing Director: Mr. Raveendran Kunnummmal Veettil
- designation: MD, CEO
- company_description: M/S INTERNATIONAL TXG PRIVATE LIMITED Technical Xperts Group is an international technology resource provider with the strength of technical expertise and 10 years of experience. Technical Xperts Group (TXG) is a venture of experts in the field of engineering, design, communication and management who has created histories in building world’s best and renowned landmarks. TXG’s industry-leading collaboration that delivers human resource support, training, technical project design, consultation and support for VDC, global engineering, CAD services and coordinated BIM modelling. TXG is committed to deliver solutions and services for leading companies across the world. Our values and professionalism in creating world class support has its own benchmark. Our comprehensive and collaborated support increases efficiency and sustainability, improve operational performance, maximize profit value, and ensure seamless incorporation of future technologies. TXG support customer growth through our customized solutions and strategies, which help us to deliver commitments. The expertise of our team, along with a strong network, is the key to our success.
- domain_expertise: International Technology service provider in the field of Engineering, design, communication and management. We are one of the pioneers in the technology of digitalizing construction industry. Utilization of Artificial Intelligence in construction industry is one of our core areas of concentration.
- cyberpark_listing_url: https://cyberparks.in/listings/m-s-international-txg-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: AI/ML / IT Services
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists AI/ML and IT Services, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in AI/ML and IT Services and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### M2H Infotech LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: We are a software product company, based out in Kerala and UAE which mainly deals with UAE Central bank compliance products like Wages Protection System(WPS) and Fund Transfer system(FTS). Bank like United Arab Bank, Al Hilal Bank, AL Masraf Bank, SWYPE Prepaid Cards are prestigious customers using our Product.
- company_name: M2H Infotech LLP.
- address: Ground Floor, Govt Cyber Park, Sahya Building
- pincode: 673014
- phone: 8891213016
- email: hr@m2hinfotech.com
- website: http://m2hinfotech.com/
- contact_name: Haris PT
- designation: MD, CEO
- company_description: We are a software product company, based out in Kerala and UAE which mainly deals with UAE Central bank compliance products like Wages Protection System(WPS) and Fund Transfer system(FTS). Bank like United Arab Bank, Al Hilal Bank, AL Masraf Bank, SWYPE Prepaid Cards are prestigious customers using our Product.
- domain_expertise: Cloud Based Hr software Solutions: Officekit HR School Management Mobile App Wages Protection System Fund Transfer System
- cyberpark_listing_url: https://cyberparks.in/listings/m2h-infotech-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / Software Development / Cloud/DevOps / Software Product
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and Software Development and Cloud/DevOps, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and Software Development and Cloud/DevOps aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### MECHANFO INTELLECT PVT. LTD..
- Audit business type: Other technology
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: Mechanfo Intellect, we create a better world enriched with sophisticated technologies that are customized according to the future needs of the society. We intend to provide services in various technological and industrial sectors in order to phase out the orbit between the industrial trends and consumer aspects. In near future our objective is to establish an ever-nourishing community which tends to serve different facets of the future society along the length and breadth of the world.
- company_name: MECHANFO INTELLECT PVT. LTD..
- address: UNIT NO:16, UB, SAHYA BUILDING, Govt Cyberpark
- pincode: 673014
- phone: 8139000256
- email: hr@mechanfo.com
- website: http://www.mechanfo.com
- contact_name: FARHAN E M
- designation: MD, CEO
- company_description: Mechanfo Intellect, we create a better world enriched with sophisticated technologies that are customized according to the future needs of the society. We intend to provide services in various technological and industrial sectors in order to phase out the orbit between the industrial trends and consumer aspects. In near future our objective is to establish an ever-nourishing community which tends to serve different facets of the future society along the length and breadth of the world.
- domain_expertise: Information & Technology,Robotics,Mechanical Engineering,Project Management
- cyberpark_listing_url: https://cyberparks.in/listings/mechanfo-intellect-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### MENTOR PERFORMANCE.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: SUPPLY CHAIN MANAGEMENT , E R P SOLUTIONS WITH MOBILE APPLICATION
- company_name: MENTOR PERFORMANCE.
- address: SAHYA Building , ROOM 21, UB FLOOR
- pincode: 673014
- phone: 9656223366
- email: hr@mentorperformance.com
- website: http://www.mentorperformance.com
- contact_name: SHIHABUDHEEN T
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: SUPPLY CHAIN MANAGEMENT , E R P SOLUTIONS WITH MOBILE APPLICATION
- cyberpark_listing_url: https://cyberparks.in/listings/mentor-performance-rating-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development
- relevant_roles: Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### MIDNAY Tech Private Limited.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Founded in 2022, MIDNAY Tech Private Limited is a software product development company based in Calicut, Kerala. MIDNAY Tech Private Limited aspires to be an industry leader in high performance web applications, developing revolutionary web application suites and web experience platforms. We at MIDNAY Tech Private Limited believe everyone has freedom to create and with our sustainable service and support, we ensure their growth with scalable web platforms.
- company_name: MIDNAY Tech Private Limited.
- address: Sahya Building, Cyberpark
- pincode: Not available in source files.
- phone: 8714142874
- email: hr@midnay.com
- website: https://midnay.com
- contact_name: Ajay
- designation: MD, CEO
- company_description: Founded in 2022, MIDNAY Tech Private Limited is a software product development company based in Calicut, Kerala. MIDNAY Tech Private Limited aspires to be an industry leader in high performance web applications, developing revolutionary web application suites and web experience platforms. We at MIDNAY Tech Private Limited believe everyone has freedom to create and with our sustainable service and support, we ensure their growth with scalable web platforms.
- domain_expertise: Web Performance Optimization Web Application Suites Web Experience Platforms
- cyberpark_listing_url: https://cyberparks.in/listings/sprintisle-digital-solutions-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Software Product
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Software Product, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Software Product aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### MKM Info Solutions Pvt. Ltd..
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: MKM Info Solutions is a leading software, mobile application and web application development company serving clients all over the world. We were established in 2013 with a group of young professionals from various disciplines with a vision of providing business to cooperate, small business utilizing software and web based technologies. Our goal is to provide innovative software and IT solutions with quality and affordable price that satisfies customer evolving needs. Our Vision is to "provide continuous value addition to our clients with the best and most innovative technologies by delivering excellent business solutions". Our experienced and expert professionals having experience in various domains, enables individuals and organizations to realize their full potential on the internet, and is provided in a range of cost models. We have an ideal and proven capability for delivering cutting edge technologies and packaged software, network and web solutions to small and medium enterprises, public and corporate clients.
- company_name: MKM Info Solutions Pvt. Ltd..
- address: Unit 1H, 2nd Floor, Sahya Building
- pincode: Not available in source files.
- phone: +919846748437
- email: hr@mkminfosolutions.com
- website: http://www.mkminfosolutions.com
- contact_name: MUNEER MELE KUNNATH , KARIKKADAN POYIL NISIYA
- designation: MD, CEO
- company_description: MKM Info Solutions is a leading software, mobile application and web application development company serving clients all over the world. We were established in 2013 with a group of young professionals from various disciplines with a vision of providing business to cooperate, small business utilizing software and web based technologies. Our goal is to provide innovative software and IT solutions with quality and affordable price that satisfies customer evolving needs. Our Vision is to "provide continuous value addition to our clients with the best and most innovative technologies by delivering excellent business solutions". Our experienced and expert professionals having experience in various domains, enables individuals and organizations to realize their full potential on the internet, and is provided in a range of cost models. We have an ideal and proven capability for delivering cutting edge technologies and packaged software, network and web solutions to small and medium enterprises, public and corporate clients.
- domain_expertise: Software Development, Web Application Development, Mobile Application Development, Ecommerce Application Development, ERP Solutions, Desktop Applications, CRM Solutions etc.
- cyberpark_listing_url: https://cyberparks.in/listings/mkm-info-solutions-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / E-commerce / Software Development / Enterprise Software
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and E-commerce, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and E-commerce aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### MYM INFOTECH LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: MYM INFOTECH LLP Excellent Insight into the business A premier IT solutions and services provider, MYM Infotech was established by a highly-qualified and enthusiastic team of IT professionals. We are committed to providing cutting-edge ERP Software, GIS Application Development, Mobile App Development, Website Design and Development. Our offices in the Middle East constantly keep abreast of the latest technological trends, assuring our clients are always a step ahead. Through our world-class ERP solutions we enable global establishments across various business functions and industries with two major business mandates: effectively manage and enhance business functions, and efficiently stay-ahead in the competitive and ever-changing world market.
- company_name: MYM INFOTECH LLP.
- address: No:13, First Basement, Sahya Cyberpark
- pincode: 673016
- phone: 7907285695
- email: info@myminfotech.com
- website: http://myminfotech.com
- contact_name: Mubashir P
- designation: MD, CEO
- company_description: MYM INFOTECH LLP Excellent Insight into the business A premier IT solutions and services provider, MYM Infotech was established by a highly-qualified and enthusiastic team of IT professionals. We are committed to providing cutting-edge ERP Software, GIS Application Development, Mobile App Development, Website Design and Development. Our offices in the Middle East constantly keep abreast of the latest technological trends, assuring our clients are always a step ahead. Through our world-class ERP solutions we enable global establishments across various business functions and industries with two major business mandates: effectively manage and enhance business functions, and efficiently stay-ahead in the competitive and ever-changing world market.
- domain_expertise: ERP Software
- cyberpark_listing_url: https://cyberparks.in/listings/mym-infotech-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / Software Development / Enterprise Software
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and Software Development and Enterprise Software, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and Software Development and Enterprise Software aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### ODOX SOFT HUB LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Odox SoftHub LLP is a leading provider of Odoo implementation and maintenance services based in Kozhikode. Our team of innovative and passionate developers is committed to pushing the boundaries of what’s possible with Odoo ERP. We offer a range of services including Odoo integration, migration, customization, training, and more. At Odox SoftHub LLP, we aim to innovate and optimize software solutions to enhance your business operations and support your growth. Our mission is to fuel your growth by delivering cutting-edge solutions that improve efficiency and drive success.
- company_name: ODOX SOFT HUB LLP.
- address: 2nd Floor, Sahya Govt CyberPark 167/A,GA College P.O
- pincode: Not available in source files.
- phone: +91 7510151792
- email: info@odoxsofthub.com
- website: http://www.odoxsofthub.com
- contact_name: Muhammad Shiyas
- designation: MD, CEO
- company_description: Odox SoftHub LLP is a leading provider of Odoo implementation and maintenance services based in Kozhikode. Our team of innovative and passionate developers is committed to pushing the boundaries of what’s possible with Odoo ERP. We offer a range of services including Odoo integration, migration, customization, training, and more. At Odox SoftHub LLP, we aim to innovate and optimize software solutions to enhance your business operations and support your growth. Our mission is to fuel your growth by delivering cutting-edge solutions that improve efficiency and drive success.
- domain_expertise: Odoo, Python. Django, Data Analytics
- cyberpark_listing_url: https://cyberparks.in/listings/odox-soft-hub-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development / Enterprise Software
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development and Enterprise Software, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development and Enterprise Software aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### ONTASH INDA TECHNOLOGIES Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Ontash was founded in 1993, when the world was just beginning to learn of the transformative power of the Internet. But even in the earliest years, it was apparent that access to unlimited amounts of data had no benefit, unless it was organized to reveal meaningful insights. With a progressive team of technologists, working out of offices in Guttenburg, NJ, Ontash has refined this ability to organize seemingly random bits of data in a variety of ways. Creating web-based platforms for branding, engaging, relationship building, buying and selling. Developing Cloud solutions, so that Fortune 500 companies can run their enterprises from desktop dashboards. Designing and developing native and hybrid mobile apps to drive retail traffic, educate, entertain and build customer relationships. Writing APIs that tame enormous government databases and reveal insights for marketing, customer service and revenue cycle decisions. Creating software for shipping companies, to automate logistics, saving time and money. Ontash currently employs 25 tech visionaries out of offices in New Jersey, India and Sri Lanka. But rather than focus exclusively on the “left brain” analytical side of technology, Ontash has also devoted considerable resources in “right brain” talent that adds a creative elements to all products and services. The objective: simple, user-friendly, well designed products that work.
- company_name: ONTASH INDA TECHNOLOGIES Pvt Ltd.
- address: Ist Floor , Unit 15 , "SAHYA" Cyberpark Kozhikode (A Govt. of Kerala Undertaking) KSITIL Special Economic Zone, Nellikkode PO, Kozhikode
- pincode: 673 016
- phone: 0495-2325399
- email: nipton@ontash.net
- website: http://www.ontash.net
- contact_name: CHARLES G THOMAS
- designation: MD, CEO
- company_description: Ontash was founded in 1993, when the world was just beginning to learn of the transformative power of the Internet. But even in the earliest years, it was apparent that access to unlimited amounts of data had no benefit, unless it was organized to reveal meaningful insights. With a progressive team of technologists, working out of offices in Guttenburg, NJ, Ontash has refined this ability to organize seemingly random bits of data in a variety of ways. Creating web-based platforms for branding, engaging, relationship building, buying and selling. Developing Cloud solutions, so that Fortune 500 companies can run their enterprises from desktop dashboards. Designing and developing native and hybrid mobile apps to drive retail traffic, educate, entertain and build customer relationships. Writing APIs that tame enormous government databases and reveal insights for marketing, customer service and revenue cycle decisions. Creating software for shipping companies, to automate logistics, saving time and money. Ontash currently employs 25 tech visionaries out of offices in New Jersey, India and Sri Lanka. But rather than focus exclusively on the “left brain” analytical side of technology, Ontash has also devoted considerable resources in “right brain” talent that adds a creative elements to all products and services. The objective: simple, user-friendly, well designed products that work.
- domain_expertise: Healthcare Solutions Enterprise Solutions Mobile Application Development Cloud Services
- cyberpark_listing_url: https://cyberparks.in/listings/ontash-inda-technologies-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / Software Development / Cloud/DevOps / Healthcare IT / Enterprise Software
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and Software Development and Cloud/DevOps, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and Software Development and Cloud/DevOps aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Pixbit Solutions Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Pixbit Solutions Pvt Ltd is guided by a team of experts with great passion for software design and development. We provides innovative and result oriented software design and development strategies to more than 100 clients from 15 countries. With vast experience in different type of technologies, our solutions consistently exceed the expectations of our clients, whether it’s a small to medium size, or large size organisations.
- company_name: Pixbit Solutions Pvt Ltd.
- address: Pixbit Solutions Pvt Ltd, Unit 4, 4th Floor, "Sahya", Govt. Cyberpark
- pincode: 673016
- phone: 7560 933 933
- email: contact@pixbitsolutions.com
- website: http://pixbitsolutions.com
- contact_name: Raisal U, Nidhin KC, Muhammed Shafi P
- designation: MD, CEO
- company_description: Pixbit Solutions Pvt Ltd is guided by a team of experts with great passion for software design and development. We provides innovative and result oriented software design and development strategies to more than 100 clients from 15 countries. With vast experience in different type of technologies, our solutions consistently exceed the expectations of our clients, whether it’s a small to medium size, or large size organisations.
- domain_expertise: • iOS and Android mobile application design and development. • Web application design and development. • Laravel development. • Enterprise Applications Development. • E-Commerce solutions design and development. • Cloud computing and hosting. • Social media and digital marketing.
- cyberpark_listing_url: https://cyberparks.in/listings/pixbit-solutions-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / E-commerce / Cloud/DevOps
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and E-commerce, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and E-commerce aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Platinum Ace Backend Solutions LLP.
- Audit business type: Non-IT / other business
- IT/ITeS: No / not established. Software development: No / not established.
- Classification evidence: Accounting Service
- company_name: Platinum Ace Backend Solutions LLP.
- address: B1, Sahya Building, KSITIL, Govt Cyber Park ,SEZ Unit , Nellikode (PO)
- pincode: 673016
- phone: 9995408708
- email: shinjith@pabsolutions.in
- website: http://www.pabsolutions.in
- contact_name: Not available in source files.
- designation: Not available in source files.
- company_description: Not available in source files.
- domain_expertise: Accounting Service
- cyberpark_listing_url: https://cyberparks.in/listings/platinum-ace-backend-solutions-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Protected Harbor Technology Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: IT Support
- company_name: Protected Harbor Technology Pvt Ltd.
- address: 20, B1,Sahya
- pincode: Not available in source files.
- phone: 9562893859
- email: sajir@protectedharbor.com
- website: http://www.protectedharbor.com
- contact_name: Fasif VP
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: IT Support
- cyberpark_listing_url: https://cyberparks.in/listings/protected-harbor-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Soxo.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Founded in March 2021, Soxo set out itself to grow as a Product development company to build tech products in healthcare and for enterprise businesses . Started with a vision to bring structure to an organization by decluttering work chaos and automation to any redundant manual work , we have products that provide solutions to streamline hospitals , clinics , retails businesses etc. At Soxo , we try to Simplify your business and try to remove the work chaos by applying engineering to your everyday work.
- company_name: Soxo.
- address: Sahya Building
- pincode: Not available in source files.
- phone: 8089224005
- email: hello@soxo.in
- website: https://soxo.in/
- contact_name: Dr Mohammed Kasim
- designation: MD, CEO
- company_description: Founded in March 2021, Soxo set out itself to grow as a Product development company to build tech products in healthcare and for enterprise businesses . Started with a vision to bring structure to an organization by decluttering work chaos and automation to any redundant manual work , we have products that provide solutions to streamline hospitals , clinics , retails businesses etc. At Soxo , we try to Simplify your business and try to remove the work chaos by applying engineering to your everyday work.
- domain_expertise: Health Care , Accounting , Automation , Product Development
- cyberpark_listing_url: https://cyberparks.in/listings/soxo/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Healthcare IT / Software Product
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Healthcare IT and Software Product, which aligns with full-stack software development.
- email_angle: Your stated work in Healthcare IT and Software Product aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Techlogica IT DT Solutions.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: Techlogica IT DT Solutions Techlogica comes with an in-depth knowledge and expertise in delivering an unrivaled portfolio of end to end ERP solutions and services that contribute business evolution and growth initiatives
- company_name: Techlogica IT DT Solutions.
- address: 2nd Floor, Sahiya Building
- pincode: 673014
- phone: 7736213919
- email: Hr@techlogica.com
- website: http://www.techlogica.com
- contact_name: Mr. Saleem Ammed, Mr. AMeer Kallil, Mr. Santo Puthoor (IT Director) and Mr. Nazir Ebrahim (HR Director
- designation: MD, CEO
- company_description: Techlogica IT DT Solutions Techlogica comes with an in-depth knowledge and expertise in delivering an unrivaled portfolio of end to end ERP solutions and services that contribute business evolution and growth initiatives
- domain_expertise: Microsoft, Linux, Android, Dot Net, Oracle, Microsoft .Net, Java, Node, Xamarin and Ignite
- cyberpark_listing_url: https://cyberparks.in/listings/techlogica-it-dt-solutions/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: Enterprise Software
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists Enterprise Software, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in Enterprise Software and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Technaureus Info Solutions Pvt. Ltd..
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Technaureus Info Solutions Pvt. Ltd. is an ISO 9001:2015 Certified software development company and ERP Implementation partner provide the application suits to empower organizations to increase business performance at all levels. We started our journey with 8+ years of experienced professionals; Technaureus is now the front-line service provider of Odoo ERP, Web & Mobile Development, Branding etc. catering both domestic and international clients. We have 100+ satisfied clients across the globe and we have implemented Odoo services in different industries such as retail, production, healthcare, travel & tourism, education, hotel & restaurant, management & consultancy, manpower supply, information & telecommunication etc. We provide our services in any size of the industry such as small, medium and large companies and also in govt, semi govt, and private sectors. Our aim is to assure the highest quality products, total client satisfaction, timely delivery of applications, and the best quality products at affordable prices.
- company_name: Technaureus Info Solutions Pvt. Ltd..
- address: Unit 2E- 2nd Floor, SahyaBuilding, Cyberpark, Nellikkode
- pincode: 673016
- phone: +91 6282608085
- email: hr@technaureus.com
- website: http://www.technaureus.com
- contact_name: Jasad Moozhiyan
- designation: MD, CEO
- company_description: Technaureus Info Solutions Pvt. Ltd. is an ISO 9001:2015 Certified software development company and ERP Implementation partner provide the application suits to empower organizations to increase business performance at all levels. We started our journey with 8+ years of experienced professionals; Technaureus is now the front-line service provider of Odoo ERP, Web & Mobile Development, Branding etc. catering both domestic and international clients. We have 100+ satisfied clients across the globe and we have implemented Odoo services in different industries such as retail, production, healthcare, travel & tourism, education, hotel & restaurant, management & consultancy, manpower supply, information & telecommunication etc. We provide our services in any size of the industry such as small, medium and large companies and also in govt, semi govt, and private sectors. Our aim is to assure the highest quality products, total client satisfaction, timely delivery of applications, and the best quality products at affordable prices.
- domain_expertise: Business Consulting , Process Re-engineering , ERP Software Development & Implementation (Odoo, Flectra, ERPNext) , Software Development , Web Development , Mobile Development , Ecommerce Development , Branding & Digital Marketing
- cyberpark_listing_url: https://cyberparks.in/listings/technaureus-info-solutions-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / E-commerce / Software Development / Healthcare IT / Enterprise Software
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and E-commerce, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and E-commerce aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### TIMESWORLD MEDIA & TECHNOLOGY.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: TIMESWORLD MEDIA & TECHNOLOGY SOLUTIONS PVT LTD Started in 2005 in the name of WebSight Computer Systems, we have been taking ourselves through a time testing expedition for several years. Currently, we are a leading provider of data management, market research, analytics and business intelligence solutions. Our core services include Data research and analysis, Database management, New technology induction, identification of innovative pathways in business processes, market research, Integration & scaling of new methods into existing systems, anti-SPAM compliant digital marketing, programming in various technologies for web and mobile applications. We are pioneers in deploying Cognitive solutions on to existing systems to make them smarter and intelligent. We observe and remain keen on finding cost effective technology solutions that can improve business performance. Our team has successfully implemented several projects all over the Middle East. With an in-depth understanding of business processes, our consultants and technocrats have delivered prestigious results to several industry segments. We also have a data management and research team based out of our development centre in India.
- company_name: TIMESWORLD MEDIA & TECHNOLOGY.
- address: Office 1, Ground Floor , Sahya Building, Cyberpark
- pincode: 673016
- phone: Not available in source files.
- email: careers@timesworld.com
- website: http://www.timesworld.com
- contact_name: TOMY VARGHESE
- designation: MD, CEO
- company_description: TIMESWORLD MEDIA & TECHNOLOGY SOLUTIONS PVT LTD Started in 2005 in the name of WebSight Computer Systems, we have been taking ourselves through a time testing expedition for several years. Currently, we are a leading provider of data management, market research, analytics and business intelligence solutions. Our core services include Data research and analysis, Database management, New technology induction, identification of innovative pathways in business processes, market research, Integration & scaling of new methods into existing systems, anti-SPAM compliant digital marketing, programming in various technologies for web and mobile applications. We are pioneers in deploying Cognitive solutions on to existing systems to make them smarter and intelligent. We observe and remain keen on finding cost effective technology solutions that can improve business performance. Our team has successfully implemented several projects all over the Middle East. With an in-depth understanding of business processes, our consultants and technocrats have delivered prestigious results to several industry segments. We also have a data management and research team based out of our development centre in India.
- domain_expertise: Data research and analysis, Database management, New technology induction, identification of innovative pathways in business processes, market research, anti-SPAM and GDPR compliance consulting, programming for web and mobile applications.
- cyberpark_listing_url: https://cyberparks.in/listings/timesworld-media-and-technology-solutions-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development
- relevant_roles: Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### TURNIPSEED ACCOUNTING Pvt. Ltd..
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: Turnipseed Accounting Private limited is a subsidiary of Turnipseed International Inc., USA. We have been conducting business with our parent Company Turnipseed International, USA for about 20 years now. Turnipseed international has been associated with the US Construction industry for more than 40 years. Turnipseed International Supplies Wood Framing hardware for Large Commercial Buildings, Motels and Restaurants and is the primary supplier for Patio Railings for Chipotle Restaurants in the United States.
- company_name: TURNIPSEED ACCOUNTING Pvt. Ltd..
- address: Unit 8 ,First Floor Sahya Building, Cyberpark Kozhikode.
- pincode: Not available in source files.
- phone: 09886365308
- email: sajith@flatworldaccounting.com
- website: http://www.turnipseed.biz
- contact_name: SAJITH MANAYILL
- designation: MD, CEO
- company_description: Turnipseed Accounting Private limited is a subsidiary of Turnipseed International Inc., USA. We have been conducting business with our parent Company Turnipseed International, USA for about 20 years now. Turnipseed international has been associated with the US Construction industry for more than 40 years. Turnipseed International Supplies Wood Framing hardware for Large Commercial Buildings, Motels and Restaurants and is the primary supplier for Patio Railings for Chipotle Restaurants in the United States.
- domain_expertise: Back office ITES Operations, Bookkeeping, Engineering Estimation, Project Management and Technology Support Services.
- cyberpark_listing_url: https://cyberparks.in/listings/turnipseed-accounting-private-limited/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### VEUZ CONCEPTS PVT.LTD.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Veuz Concepts is a global Information Technology company which provides technology solutions to our distinguished customers in India and Middle East since 2008, spanning a range of IT verticals. As a startup company in its early years, we were one of the few selected for the Government supported Startup Village in Cochin. We are powered with the best talent and most modern technologies for online and offline solutions that help businesses move forward, right from developing people friendly websites, intelligent software solutions & mobile applications, and branding solutions for small to large enterprises. To achieve success, Veuz Concepts adheres to the following set of goals with each client: • We listen to you. You know your customer best. • We utilize our years of experience to provide you with proven solutions. • We ensure future-proof design and functionality by using best-practice techniques. Times may change, but our service will stay sleek and relevant. Our Global Delivery Model provides for the best resources to be drawn from its vast talent pool across the globe to offer optimal solutions.
- company_name: VEUZ CONCEPTS PVT.LTD.
- address: Unit 6, Ground Floor, Sahya Building
- pincode: Not available in source files.
- phone: 9544 33 1111
- email: hr@veuz.in , support@veuz.in
- website: http://www.veuzconcepts.com
- contact_name: MOHAMMED NAVAB
- designation: MD, CEO
- company_description: Veuz Concepts is a global Information Technology company which provides technology solutions to our distinguished customers in India and Middle East since 2008, spanning a range of IT verticals. As a startup company in its early years, we were one of the few selected for the Government supported Startup Village in Cochin. We are powered with the best talent and most modern technologies for online and offline solutions that help businesses move forward, right from developing people friendly websites, intelligent software solutions & mobile applications, and branding solutions for small to large enterprises. To achieve success, Veuz Concepts adheres to the following set of goals with each client: • We listen to you. You know your customer best. • We utilize our years of experience to provide you with proven solutions. • We ensure future-proof design and functionality by using best-practice techniques. Times may change, but our service will stay sleek and relevant. Our Global Delivery Model provides for the best resources to be drawn from its vast talent pool across the globe to offer optimal solutions.
- domain_expertise: Application Development & Maintenance, Mobility Solutions, Business Services (Oracle ERP, Salesforce, Zoho), Digital Marketing, UI/UX, Web Hosting & Email Services (AWS, Google, Microsoft, Yahoo, Custom Solutions)
- cyberpark_listing_url: https://cyberparks.in/listings/veuz-concepts-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Mobile Development / Software Development / Enterprise Software
- relevant_roles: Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Mobile Development and Software Development and Enterprise Software, which aligns with full-stack software development.
- email_angle: Your stated work in Mobile Development and Software Development and Enterprise Software aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Vinam Solutions Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: COMPANY PROFILE : Â A booming software development service provider with it's corporate office at Unit-5, IT building, Government Cyber Park, Kozhikode, Kerala, India and it's registered office at Hilite Business Park, Kozhikode, Kerala, India, Vinam Solutions is an all in one solution for your complete IT requirements.Established in the year 2013, the company has earned an admirable reputation in the IT & Marketing industry with its powerful growth aspects by acquiring some of the key projects in the shortest feasible period. Embraced with a team of amazing professionals who is keen on providing complete IT solutions under one roof, Vinam Solutions is now a highly recommended IT provider in the industry. Vinamâ€™s expansion has been extended to The United Kingdom by opening a new office in London, and it is also the parent firm of Luvia, one of the most seeked Global marketing agency in Digital Marketing. Vinam Solutions offers the clients the widest spectrum of services on development, maintenance and promotion of websites. Vinam has been able to make a name for itself and it was only possible because of its ability and commitments to ensure customer satisfaction by rewarding on time and accurate delivery. We are committed to prompt services to our clients and innovative developments.
- company_name: Vinam Solutions Pvt Ltd.
- address: Unit-5, IT Building, KSITIL Special Economic Zone, Government Cyber Park, Kozhikode, Kerala, India
- pincode: 673016
- phone: +91 9745005454, +91 04952436700
- email: info@vinamsolutions.com
- website: http://www.vinam.in
- contact_name: Vinoop T
- designation: MD, CEO
- company_description: COMPANY PROFILE : Â A booming software development service provider with it's corporate office at Unit-5, IT building, Government Cyber Park, Kozhikode, Kerala, India and it's registered office at Hilite Business Park, Kozhikode, Kerala, India, Vinam Solutions is an all in one solution for your complete IT requirements.Established in the year 2013, the company has earned an admirable reputation in the IT & Marketing industry with its powerful growth aspects by acquiring some of the key projects in the shortest feasible period. Embraced with a team of amazing professionals who is keen on providing complete IT solutions under one roof, Vinam Solutions is now a highly recommended IT provider in the industry. Vinamâ€™s expansion has been extended to The United Kingdom by opening a new office in London, and it is also the parent firm of Luvia, one of the most seeked Global marketing agency in Digital Marketing. Vinam Solutions offers the clients the widest spectrum of services on development, maintenance and promotion of websites. Vinam has been able to make a name for itself and it was only possible because of its ability and commitments to ensure customer satisfaction by rewarding on time and accurate delivery. We are committed to prompt services to our clients and innovative developments.
- domain_expertise: Software Development ; Digital Marketing
- cyberpark_listing_url: https://cyberparks.in/listings/vinam-solutions-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Wattlecorp Cybersecurity Labs LLP.
- Audit business type: Other technology
- IT/ITeS: Yes. Software development: No / not established.
- Classification evidence: Wattlecorp Cybersecurity Labs is a provider of Cybersecurity solutions, specializing in cutting-edge Cybersecurity solutions and services that help businesses become more Cyber resilient. If you require a quick security check-up, a comprehensive security assessment, or ongoing Cybersecurity support, Wattlecorp has the solution. We specialize in VAPT,Vulnerability assessment and penetration testing and believe that the bottom-line benefits of investing in Cybersecurity are that you get that customary assurance that you are approaching Cybersecurity in the right way, that you get that competitive advantage that you are doing the things that customers expect you to do, and that you are ultimately securing your business
- company_name: Wattlecorp Cybersecurity Labs LLP.
- address: Unit no 8, Sahya Building, UB
- pincode: 673014
- phone: +91 8289885662
- email: info@wattlecorp.com
- website: https://www.wattlecorp.com/
- contact_name: Kalathil Karthik, Zuhair E
- designation: MD, CEO
- company_description: Wattlecorp Cybersecurity Labs is a provider of Cybersecurity solutions, specializing in cutting-edge Cybersecurity solutions and services that help businesses become more Cyber resilient. If you require a quick security check-up, a comprehensive security assessment, or ongoing Cybersecurity support, Wattlecorp has the solution. We specialize in VAPT,Vulnerability assessment and penetration testing and believe that the bottom-line benefits of investing in Cybersecurity are that you get that customary assurance that you are approaching Cybersecurity in the right way, that you get that competitive advantage that you are doing the things that customers expect you to do, and that you are ultimately securing your business
- domain_expertise: Vulnerability Assessment and Penetration Testing Security Operation Center IT Risk Management Managed Security Security Information & Event Management
- cyberpark_listing_url: https://cyberparks.in/listings/wattlecorp-cybersecurity-labs-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Medium
- developer_relevance: Medium
- primary_technology_area: Cybersecurity
- relevant_roles: Not available in source files.
- priority: Medium
- job_match_reason: Technology-relevant match because Cyberpark lists Cybersecurity, though direct software-development activity is not clearly stated.
- email_angle: I’m interested in your stated work in Cybersecurity and its possible overlap with software development.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Welkinwits technologies llp.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Software Development, Custom Business Solutions, Mobile Application Development , Web Application & Portals , Wits-Cloud Projects
- company_name: Welkinwits technologies llp.
- address: 3rd floor , Sahya building, Govt cyberpark
- pincode: 673016
- phone: 9142859323
- email: md@welkinwitstech.com
- website: http://www.welkinwitstech.com
- contact_name: MUHAMMED IRFAN VV, SUSHANTH JAYARAJ
- designation: MD, CEO
- company_description: Not available in source files.
- domain_expertise: Software Development, Custom Business Solutions, Mobile Application Development , Web Application & Portals , Wits-Cloud Projects
- cyberpark_listing_url: https://cyberparks.in/listings/welkinwits-technologies-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / Software Development / Cloud/DevOps
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Software Developer, Software Engineer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and Software Development, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and Software Development aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### YouGotaGift Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: YouGotaGift Pvt Ltd is the leading Digital Gift Card Company in the Middle East. Our digital gifting platform is used by individuals and businesses to celebrate, reward, motivate and show appreciation to friends, loved ones, employees, customers and business partners. Our business solution has also been adopted by major customer loyalty programs across leading telcos, banks, airlines delivering an unparalleled choice of rewards, a memorable customer service experience, and best-in-class technology tailored to partner needs. YouGotaGift is a well established product company, we take utmost importance on the technology stack we use, our goal is to run our products on proven latest technologies in its proper way. A few of our products: eGift API: A product being used by large-scale corporates like Uber, Etisalat, almost all of the banks in the middle east and many more. We have close to 300 large-scale corporate clients using this product. Rewards: A product being used by clients like Smart Dubai, iPsos, Nielsen ( Research Companies ) and more, we have close to 200 corporate clients in this product. MyRewards: A dedicated product for companies such as MasterCard. The product is being used to power the banks who have issued MasterCard Debit / Credit Cards. The transactions are huge, easily reaching a few millions in a day. We have many more well established private products being used by large-scale corporates . As part of our expansion plan, we have opened our Offshore development centre ( YouGotaGift Pvt Ltd ) in Calicut, Kerala, by providing the best in class facilities and benefits to our employees.
- company_name: YouGotaGift Pvt Ltd.
- address: Unit-19, First floor, Sahya Building
- pincode: Not available in source files.
- phone: Not available in source files.
- email: careers-clt-ind+cyberpark@yougotagift.com
- website: https://yougotagift.com
- contact_name: Ashin K N, Husain K M
- designation: MD, CEO
- company_description: YouGotaGift Pvt Ltd is the leading Digital Gift Card Company in the Middle East. Our digital gifting platform is used by individuals and businesses to celebrate, reward, motivate and show appreciation to friends, loved ones, employees, customers and business partners. Our business solution has also been adopted by major customer loyalty programs across leading telcos, banks, airlines delivering an unparalleled choice of rewards, a memorable customer service experience, and best-in-class technology tailored to partner needs. YouGotaGift is a well established product company, we take utmost importance on the technology stack we use, our goal is to run our products on proven latest technologies in its proper way. A few of our products: eGift API: A product being used by large-scale corporates like Uber, Etisalat, almost all of the banks in the middle east and many more. We have close to 300 large-scale corporate clients using this product. Rewards: A product being used by clients like Smart Dubai, iPsos, Nielsen ( Research Companies ) and more, we have close to 200 corporate clients in this product. MyRewards: A dedicated product for companies such as MasterCard. The product is being used to power the banks who have issued MasterCard Debit / Credit Cards. The transactions are huge, easily reaching a few millions in a day. We have many more well established private products being used by large-scale corporates . As part of our expansion plan, we have opened our Offshore development centre ( YouGotaGift Pvt Ltd ) in Calicut, Kerala, by providing the best in class facilities and benefits to our employees.
- domain_expertise: Digital gift card, Loyalty Rewards, Employee Rewards, Consumer Gifting. ( Python, Django, ReactJS, GraphQL, AWS )
- cyberpark_listing_url: https://cyberparks.in/listings/yougotagift-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: Low
- developer_relevance: Low
- primary_technology_area: Other
- relevant_roles: Not available in source files.
- priority: Low
- job_match_reason: Cyberpark’s listing does not provide enough stated software-development activity to establish a strong match.
- email_angle: Cyberpark’s listing does not provide a specific software-development outreach angle.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Zennode Technologies LLP.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: ZenNode is a software product development company providing high-end WordPress extensions, themes and cloud-based applications to customers’ around the globe. Our team of efficient and experienced creative and engineering professionals are specialized in producing software to assist customers to operate their entire web presence smoothly. In each step of the development process, we use creative thinking, cutting-edge technologies and proven methodologies to ensure that the best is always given to the customers in terms of service and support, and thereby help the enterprise to meet an extensive growth rate.
- company_name: Zennode Technologies LLP.
- address: Unit 16, 1st Floor, Sahya Building, Govt. Cyberpark,
- pincode: Not available in source files.
- phone: 8129005599
- email: hr@zennode.com
- website: https://www.zennode.com
- contact_name: Sajeer TK
- designation: MD, CEO
- company_description: ZenNode is a software product development company providing high-end WordPress extensions, themes and cloud-based applications to customers’ around the globe. Our team of efficient and experienced creative and engineering professionals are specialized in producing software to assist customers to operate their entire web presence smoothly. In each step of the development process, we use creative thinking, cutting-edge technologies and proven methodologies to ensure that the best is always given to the customers in terms of service and support, and thereby help the enterprise to meet an extensive growth rate.
- domain_expertise: Software Development
- cyberpark_listing_url: https://cyberparks.in/listings/zennode-technologies-llp/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Software Development / Cloud/DevOps / Software Product
- relevant_roles: Software Developer, Software Engineer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Software Development and Cloud/DevOps and Software Product, which aligns with full-stack software development.
- email_angle: Your stated work in Software Development and Cloud/DevOps and Software Product aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

### Zinfog Codelabs Pvt Ltd.
- Audit business type: IT/ITeS
- IT/ITeS: Yes. Software development: Yes.
- Classification evidence: Zinfog Codelabs is a technology expert working in association with a Global partner iTAG Technologies LLC, Dubai, UAE. We follow a systematic method of development and implementation that reflects quality at every stage. We give utmost importance to the end user satisfaction with prominence to long lasting customer relationship by providing optimum support to every client. Our aim is to work with our clients by embracing their products marketing and communication strategies to develop applications that convey their key concepts and values in a diverse and perfect manner.
- company_name: Zinfog Codelabs Pvt Ltd.
- address: 1st Floor, Sahya, Govt Cyberpark, KSITIL SEZ, Nellikode PO, Kozhikode, India - 673016
- pincode: Not available in source files.
- phone: 9778965477
- email: hr@zinfog.com
- website: http://www.zinfog.com
- contact_name: Abdul Basith,Vivek T
- designation: MD, CEO
- company_description: Zinfog Codelabs is a technology expert working in association with a Global partner iTAG Technologies LLC, Dubai, UAE. We follow a systematic method of development and implementation that reflects quality at every stage. We give utmost importance to the end user satisfaction with prominence to long lasting customer relationship by providing optimum support to every client. Our aim is to work with our clients by embracing their products marketing and communication strategies to develop applications that convey their key concepts and values in a diverse and perfect manner.
- domain_expertise: Odoo Implementation and Customization, Cloud Backups, Open Source Web Application & Mobile Applications extending our hands to AI & ML
- cyberpark_listing_url: https://cyberparks.in/listings/zinfog-codelabs-pvt-ltd/
- source_url: https://cyberparks.in/companies-at-park/
- it_relevance: High
- developer_relevance: High
- primary_technology_area: Web Development / Mobile Development / AI/ML / Cloud/DevOps
- relevant_roles: Full-Stack Developer, Web Developer, Frontend Developer, Backend Developer, Mobile Developer
- priority: High
- job_match_reason: Strong match because Cyberpark describes the company’s work as Web Development and Mobile Development and AI/ML, which aligns with full-stack software development.
- email_angle: Your stated work in Web Development and Mobile Development and AI/ML aligns closely with my full-stack software development experience.
- research_status: success
- notes: Not available in source files.
- base_file_location: Kozhikode, Kerala
- source_filenames: cyberpark_companies.csv; cyberpark_company_enriched.csv

## 7. IT/ITeS Companies

Adam Finastra Private Limited.; Axel Technologies Pvt Ltd.; Freston Analytics Private Limited..; Gritstone Technologies LLP.; IPIX TECH SERVICES PVT LTD.; Lenok Solutions.; Logiology Solutions Pvt. Ltd..; Medaura Infotech PVT LTD.; MOJGENIE IT SOLUTIONS PRIVATE LIMITED.; Pfactorial Technologies Pvt Ltd.; Sapling Creations Private Limited.; Tigabits Technologies LLP.; VIKN CODES.; Yarddiant Weblounge Pvt Ltd.; ZOONDIA.; ABANA Technology Private Limited.; Acadeno Technologies Private Limited.; Analystor Technologies.; Artifitia Solutions LLP.; Aufait Technologies Pvt Ltd.; BPRACT.; CODESAP TECHNOLOGIES LLP.; Codilar Technologies Pvt.Ltd.; Doctosmart.; ERE BUSINESS SOLUTIONS PV LTD.; eSynergy Technologies Pvt Ltd.; Fantacode Private Limited.; GETLEAD ANALYTICS PVT LTD.; Globit Business Solutions Private Limited.; Infinite Open Source Solutions LLP ™.; IOCOD INFOTECH PVT LTD.; ioNob Innovations LLP.; John & Smith Solutions Private Limited.; Keype Systems Pvt Ltd.; LeEYE-T Techno Hub LLP.; Lilac Infotech Pvt. Ltd..; Limenzy Technologies Pvt Ltd.; Lithos Technosoft Pvt Ltd.; Logiqdreams LLP.; Loudchilli.; LRG INTERNATIONAL PRIVATE LIMITED.; M2H Infotech LLP.; MENTOR PERFORMANCE.; MIDNAY Tech Private Limited.; MKM Info Solutions Pvt. Ltd..; MYM INFOTECH LLP.; ODOX SOFT HUB LLP.; ONTASH INDA TECHNOLOGIES Pvt Ltd.; Pixbit Solutions Pvt Ltd.; Protected Harbor Technology Pvt Ltd.; Soxo.; Techlogica IT DT Solutions.; Technaureus Info Solutions Pvt. Ltd..; TIMESWORLD MEDIA & TECHNOLOGY.; TURNIPSEED ACCOUNTING Pvt. Ltd..; VEUZ CONCEPTS PVT.LTD.; Vinam Solutions Pvt Ltd.; Wattlecorp Cybersecurity Labs LLP.; Welkinwits technologies llp.; YouGotaGift Pvt Ltd.; Zennode Technologies LLP.; Zinfog Codelabs Pvt Ltd.

## 8. Software Development Companies

Adam Finastra Private Limited.; Axel Technologies Pvt Ltd.; Gritstone Technologies LLP.; IPIX TECH SERVICES PVT LTD.; Logiology Solutions Pvt. Ltd..; Medaura Infotech PVT LTD.; MOJGENIE IT SOLUTIONS PRIVATE LIMITED.; Pfactorial Technologies Pvt Ltd.; Sapling Creations Private Limited.; Tigabits Technologies LLP.; VIKN CODES.; Yarddiant Weblounge Pvt Ltd.; ZOONDIA.; ABANA Technology Private Limited.; Acadeno Technologies Private Limited.; Analystor Technologies.; Artifitia Solutions LLP.; Aufait Technologies Pvt Ltd.; BPRACT.; CODESAP TECHNOLOGIES LLP.; Codilar Technologies Pvt.Ltd.; ERE BUSINESS SOLUTIONS PV LTD.; eSynergy Technologies Pvt Ltd.; Fantacode Private Limited.; Infinite Open Source Solutions LLP ™.; IOCOD INFOTECH PVT LTD.; ioNob Innovations LLP.; John & Smith Solutions Private Limited.; Keype Systems Pvt Ltd.; LeEYE-T Techno Hub LLP.; Lilac Infotech Pvt. Ltd..; Limenzy Technologies Pvt Ltd.; Lithos Technosoft Pvt Ltd.; Logiqdreams LLP.; Loudchilli.; M2H Infotech LLP.; MIDNAY Tech Private Limited.; MKM Info Solutions Pvt. Ltd..; MYM INFOTECH LLP.; ODOX SOFT HUB LLP.; ONTASH INDA TECHNOLOGIES Pvt Ltd.; Pixbit Solutions Pvt Ltd.; Soxo.; Technaureus Info Solutions Pvt. Ltd..; TIMESWORLD MEDIA & TECHNOLOGY.; VEUZ CONCEPTS PVT.LTD.; Vinam Solutions Pvt Ltd.; Welkinwits technologies llp.; YouGotaGift Pvt Ltd.; Zennode Technologies LLP.; Zinfog Codelabs Pvt Ltd.

## 9. Other Technology Companies

D4 Integrated Security Solutions LLP.; LUZIA LAB LLP.; Coddle Technologies Private Limited.; M/S INTERNATIONAL TXG PRIVATE LIMITED.; MECHANFO INTELLECT PVT. LTD..; Wattlecorp Cybersecurity Labs LLP.

## 10. Non-IT and Unclassified Companies

Non-IT: CodeAce IT Solutions; Eljo Services; CADMUS Engineering Services; CRONUS Steel Detailing; Platinum Ace Backend Solutions. Unknown/insufficient evidence: Coddle Technologies; Dezen Consultants International; EDUMPUS PORTAL; GJ Global IT Ventures. Coddle has conflicting broad technology domains and a Risk Assessment and Design Solutions description; Dezen and EDUMPUS lack description/domain data; GJ lists domains without a clear activity.

## 11. Services and Business Capabilities

The records document custom, web, mobile, cloud, ERP, CRM, SaaS and enterprise software; AI/ML, analytics, IoT, blockchain, automation and cybersecurity; e-commerce; healthcare, finance, education, retail, HR, logistics and construction solutions; IT consulting, infrastructure and support; UI/UX, hosting, branding and digital marketing; engineering detailing, accounting and remote business management. Refer to the per-company fields for traceable attribution.

## 12. CEO and Leadership Directory

Every supplied `contact_name` and `designation` is retained in its company entry. These mixed leadership/contact fields are not independently verified as current CEO, MD, founder, or director information. Aufait Technologies Pvt Ltd and Platinum Ace Backend Solutions LLP have no supplied leadership/contact or designation.

## 13. Duplicate Audit Report

All 75 companies are confirmed exact-name duplicate pairs across the two company CSVs; no similar-name records were merged. Formatting differences within source names, including capitalization, terminal double periods, and the trademark mark in Infinite Open Source Solutions, are retained and do not create additional entities. The paired source fields do not conflict; Coddle is a classification ambiguity, not a cross-file identity conflict.

## 14. Data Quality and Missing Information

Descriptions are missing for Lenok, ABANA, CODESAP, Codilar, CRONUS, Dezen, EDUMPUS, GJ Global, Keype, LRG, Platinum Ace, Protected Harbor, and Welkinwits. Domain expertise is missing for Dezen and EDUMPUS. Individual blank contact/location fields are retained as Not available in source files. The error log reports one skipped unnamed card.

## 15. AI JobHunt Integration

Use this as the primary human-readable reference. Keep IT/ITeS and software-development separate; retain unknowns; suppress duplicate source rows in downstream reporting; retain provenance; and do not treat this Markdown as structured machine input without a defined and validated schema. Preserve source files unless separately authorized, and do not assume data remains current.

## 16. Source of Truth and Trust Limitations

This README is authoritative only as a consolidation of the three audited files. It does not independently verify identity, service, website, contact, leadership, classification, accuracy, or currency. External verification requires separately authorized work.

## 17. Maintenance Guidelines

Audit all three files before updates; reconcile records without losing fields; preserve provenance; reassess evidence-based classifications; recalculate counts; keep unknowns/conflicts visible; and never invent missing data or silently modify the original CSVs.



