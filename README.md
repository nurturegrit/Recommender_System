# JhakaasRecommender: Intelligent News Recommendation System

## What is JhakaasRecommender?

Online news reading has gained immense popularity, offering readers access to articles from millions of sources worldwide. However, the overwhelming volume of content can make it challenging for users to discover relevant and engaging articles. Addressing this issue, **JhakaasRecommender** is a cutting-edge personalized news recommendation system designed to provide a unique and engaging experience for its users.

Targeted at working professionals aged 21–40, JhakaasRecommender focuses on overcoming critical challenges such as user retention. Recognizing that a user’s first impression of the platform heavily influences their engagement, the system aims to captivate users from their very first visit by presenting a curated selection of captivating and relevant news stories.

The main website is built using the **Django framework**, ensuring a scalable, reliable, and efficient backend. Additionally, user authentication is streamlined through **Google Auth**, enabling a secure and hassle-free sign-in experience.

---

## Problem Statement
News recommendations must perform well on fresh content: breaking news that hasn’t been viewed by many readers yet. Thus we need to leverage on the article content data available at publishing time, such as topics, categories, and tags, to build a content-based model, and match it to readers’ interests learnt from their reading histories. However, one drawback of the content-based recommendations is that when there’s not enough history about a user, the coverage of the recommendations will become very limited, which is the common cold-start problem in recommender systems.
When users first interact with JhakaasRecommender, their interests and demographics are unknown, creating a "cold start" scenario. It has been seen that engagement drops sharply beyond the initial set of displayed stories unless a user clicks on one of the initial recommendations.
To address this challenge, JhakaasRecommender employs two intelligent components:

1. **Article Recommender Bot**:  Responsible for selecting the most relevant stories based on the available news corpus and any user profile data, if available.
2. **User Profiler Bot**:  Designed to analyze the user's clickstream data to infer preferences and build detailed user profiles for personalized recommendations in subsequent visits.
  
The overarching goals are to:
- Minimize bias in the data collected during the first visit (e.g., positional bias from article ranking).
- Learn as much as possible about user interests from their initial interactions.
- Maximize the coverage of the news corpus while optimizing clickthrough rates(CLR).

---

## Project Implementation
The implementation of JhakaasRecommender is divided into three key stages, ensuring a structured approach to handling data, profiling, and recommendation generation.

### 1. Preprocessing and Data Management
This stage establishses the foundation for the recommendation system by organizing and preparing the news corpus for further analysis. The **Scrapping_Data** folder serves as the repository for news articles stored in CSV format. These articles undergo rigorous preprocessing to ensure they are clean, relevant, and structured for profiling.

The preprocessing involves several critical steps:

- **Data Consolidation**: New articles are continuously added to the existing corpus, creating a comprehensive dataset that captures both historical and fresh content.
- **Deduplication**:  Articles are checked for duplicates to prevent redundant entries that may skew recommendations.
- **Temporal Filtering**:Only articles from the last seven days are retained to ensure the recommendations stay current and relevant.

These preprocessing tasks are automated using Python scripts, ensuring efficiency and consistency in data handling. The process is further documented in Jupyter notebooks, which provide an interactive environment for testing and refining the pipeline. These notebooks also include visualizations and logs to track the preprocessing progress and outcomes.

### 2. Article and User Profiling
Profiling is a pivotal stage in the system, as it creates structured representations of articles and users, which form the backbone of the recommendation engine.

#### Article Profiling
Articles are transformed into comprehensive profiles using advanced **natural language processing (NLP) techniques**. Key tasks in this phase include:

- **Embedding Generation**:  Each article is analyzed to create embeddings using BERT or similar models. These embeddings capture the semantic meaning and temporal relevance of the articles, ensuring that the system understands both their content and their contextual significance.
- **Topic Categorization**: The system clusters articles into various topics, ensuring a diverse range of content is available for recommendation.
- **Temporal Relevance**:Time embeddings are incorporated to prioritize articles that are not only relevant in content but also timely.

The resulting profiles are stored in a structured format that allows the system to quickly match articles to user interests or group dynamics.
  
#### User Profiling
User profiling begins as soon as a user interacts with the system. The clickstream data, including details such as which articles were clicked, how much time was spent, and the rank of the articles served, is analyzed to extract meaningful patterns. Key tasks include:
- **Preference Extraction**:Metrics such as clickthrough rates, time spent, and engagement levels are used to infer user preferences.
- **Bias Analysis**: The system accounts for positional biases (e.g., higher-ranked articles being more likely clicked) to avoid skewing the profile.
- **Dynamic Updates**:User profiles are updated continuously based on new interactions, ensuring that the system adapts to evolving preferences.
  
These user profiles are essential for personalization in future visits, enabling the system to recommend content that aligns closely with the user's demonstrated interests.

By combining robust preprocessing with detailed profiling, JhakaasRecommender ensures that its recommendation engine operates with clean, structured, and actionable data, paving the way for accurate and engaging recommendations
  
### 3. Recommendation Strategies
The recommendation engine employs a **hybrid approach** that integrates **content-based filtering** and collaborative filtering to provide users with personalized and diverse recommendations. To ensure optimal performance, a **multi-armed bandit strategy** is utilized. This strategy strikes a balance between exploration—introducing users to new or untested articles—and **exploitation**, which involves delivering articles known to resonate with the user based on past behavior. This balance is particularly critical during a user's first interaction with the system, where understanding preferences is still in its initial stages.


## Evaluation Metrics

The performance and effectiveness of the recommendation engine, referred to as **JhakaasRecommender**, are assessed through the following key metrics:
1. **Engagement Metrics**:These include indicators such as clickthrough rate (CTR), session duration, and user return rates, which measure how actively users interact with the recommendations.
2. **Exploration-Exploitation Balance**: This evaluates the system’s ability to optimize recommendations by catering to both established user preferences and encouraging the discovery of new interests.
3.**Coverage Metrics**: This metric tracks the percentage of the overall news corpus utilized in generating recommendations, ensuring a wide variety of content is leveraged.
---

## Technical Framework

The project adopts a modular architecture, with each component tailored to a specific function. This structure promotes scalability and ease of maintenance:
- **Preprocessing Folder**:  Houses scripts and Jupyter notebooks responsible for cleaning, organizing, and preparing the news articles and user data. These preprocessing steps ensure the data is ready for profiling and recommendation generation
- **Profiling Notebooks**:
  - `Article_Profiling.ipynb`: Focuses on analyzing and profiling individual articles, extracting features such as topics, keywords, and metadata that inform content-based filtering.
  - `User_Profiling.ipynb`:Models user behavior by analyzing their interaction patterns, preferences, and historical data. 
- **Recommendation Techniques**:Dedicated notebooks implement various recommendation strategies, including content-based filtering, collaborative filtering, and their hybrid integration. Each notebook encapsulates a specific recommendation technique, allowing for independent testing and iteration.

This well-defined framework not only enhances the system's flexibility and efficiency but also ensures a robust foundation for future enhancements and scalability.

---

## Conclusion

JhakaasRecommender effectively tackles the critical cold-start challenge by employing a robust hybrid filtering mechanism combined with dynamic user profiling. This approach ensures that even first-time users are presented with engaging and relevant news recommendations, creating a seamless and personalized experience from the outset. By integrating content-based and collaborative filtering techniques, the system capitalizes on the strengths of both methodologies, providing a balanced mix of known user preferences and opportunities to explore new content.
Moreover, JhakaasRecommender goes beyond delivering recommendations by actively minimizing biases, ensuring diverse content exposure, and maximizing coverage of the news corpus. This not only enhances the variety and inclusiveness of the recommendations but also contributes to user satisfaction and trust in the system. The implementation of a multi-armed bandit strategy further strengthens the engine’s ability to optimize the trade-off between exploration and exploitation, driving long-term user engagement and retention.
Through its innovative architecture and focus on user-centric design, JhakaasRecommender sets a new benchmark for intelligent news delivery. It leverages advanced evaluation metrics, such as clickthrough rates, session durations, and exploration-exploitation balance, to continuously refine its performance. As a result, the system achieves its goal of fostering meaningful interactions with news content while adapting to evolving user behaviors.
In redefining the standards of recommendation systems, JhakaasRecommender not only meets the immediate needs of its users but also lays the groundwork for scalable and adaptable solutions in the dynamic landscape of personalized news delivery. Its combination of innovation, precision, and user focus positions it as a trailblazer in intelligent recommendation technology.




