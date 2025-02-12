# Skincare Recommendation System Design

## 1. System Architecture

The system consists of three main components:

- **Frontend (Streamlit)**: Collects user inputs, communicates with the backend, and displays recommendations.
- **Backend (Flask/FastAPI)**: Hosts the machine learning model, processes requests, and returns product recommendations.
- **Machine Learning Model**: Pre-trained recommendation model based on the Skin-Care-Recommender-System from GitHub.

## 2. User Interaction Flow

1. **User Input**:
   - Users provide information such as skin type, concerns (e.g., acne, dryness), age, and budget range via a Streamlit UI.
   - User clicks the "Get Recommendations" button.

2. **Backend Processing**:
   - Streamlit sends a POST request to the backend API with the user’s data.
   - The backend validates and preprocesses the data.
   - The backend queries the ML model and retrieves product recommendations.

3. **Recommendation Display**:
   - Backend returns the recommended products as a JSON response.
   - Streamlit displays these recommendations in a user-friendly format (e.g., cards with product images, names, prices, and ratings).

## 3. Specification Document

### Project Overview

The skincare recommendation system is designed to provide users with tailored skincare product suggestions based on their unique characteristics such as skin type, age, and concerns. The project applies MLOps principles to ensure the model and application are scalable, maintainable, and reliable.

### Objectives

1. Develop a machine learning-based recommendation system using the Skin-Care-Recommender-System project.
2. Implement a user-friendly interface using Streamlit for collecting user preferences.
3. Establish a robust backend with Flask/FastAPI to manage model interactions and ensure scalability.
4. Provide an API endpoint for processing user input and delivering recommendations.
5. Host the project locally and prepare for potential cloud deployment.

### Functional Requirements

- **Input**: Collect user data including skin type, concerns, age, and budget.
- **Processing**: Validate input, preprocess data, and query the recommendation model.
- **Output**: Return a list of recommended products including details like name, brand, price, rating, and an image URL.

### Non-Functional Requirements

- **Performance**: The system must provide recommendations within 2 seconds of submission.
- **Scalability**: The backend should support up to 50 concurrent users.
- **Reliability**: Ensure 99% uptime when hosted locally.
- **Usability**: The UI must be intuitive for non-technical users.

### Constraints

- The model is based on a pre-trained version of the Skin-Care-Recommender-System.
- The application will be hosted locally on the user's desktop with a designated hostname.

### Deliverables

1. Functional web application (frontend + backend).
2. Deployed and tested local setup.
3. Specification document and UML diagrams.

## 4. UML Diagrams

### Component Diagram

```text
+-----------------+          +--------------------+          +---------------------+
|   Frontend      |          |     Backend        |          |     ML Model        |
| (Streamlit)     |  HTTP    | (Flask/FastAPI)    |  Query   | (Recommendation     |
|-----------------|--------->|--------------------|--------->|  Engine - Python    |
| User Input      |          | API Endpoint       |          | Pre-trained Model   |
| Display Output  |<---------| Process Request    |<---------| Prediction          |
+-----------------+          +--------------------+          +---------------------+
```

### Sequence Diagram

```text
User -> Frontend: Provide skincare preferences
Frontend -> Backend: Submit user input (POST /api/recommend)
Backend -> ML Model: Preprocess and query model
ML Model -> Backend: Return recommended products
Backend -> Frontend: Send recommendations (JSON response)
Frontend -> User: Display recommendations
```

### Class Diagram

```text
+----------------+       +------------------+       +------------------+
| UserInput      |       | Recommendation  |       | Product          |
|----------------|       |------------------|       |------------------|
| skin_type      |       | model: MLModel  |       | name: string     |
| concerns       |       | preprocess()    |       | brand: string    |
| age            |       | predict()       |       | price: float     |
| budget         |       | format_results()|       | rating: float    |
+----------------+       +------------------+       +------------------+
```

The component diagram shows the interaction between the frontend, backend, and ML model. The sequence diagram illustrates the flow of user interactions, and the class diagram outlines the relationships between key system classes.
