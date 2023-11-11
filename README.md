# Region Intelligence 

## Introduction

Welcome to the official GitHub repository for Region Intelligence, the leading platform transforming municipal real-estate development insights!

## About Us

Founded in August 2023, Region Intelligence was conceived by a group of dedicated real estate and tech enthusiasts. Recognizing a crucial gap in the market, we embarked on a mission to aggregate and simplify access to municipal real-estate development information.

### Our Journey

- **Aug 2023**: The inception of Region Intelligence. 
- **September 2023**: After a month of brainstorming and ideation, we developed our first proof of concept.
- **November 2023**: Using the feedback from our initial proof of concept, we developed our beta version, integrating enhanced data analytics capabilities and a user-friendly interface.
- **December 2023**: A closed beta test was initiated, inviting key industry professionals for rigorous testing and feedback.
- **January 2023**: With insights from our beta testers and continuous improvements, we will launch V1 of our platform. 

## Features

- **Data Aggregation**: Seamless integration with multiple municipal data sources, offering a comprehensive view of real-estate developments and re-zoning projects.
- **User-Friendly Interface**: Navigating complex municipal data has never been easier.
- **Robust Analytics**: Dive deep into data trends with our robust analytical tools, tailored for industry professionals.

## Main Projects in the Works

1. **Map**: This folder contains the code and pipeline to gather and process current planning projects from orange county cities. The data is then used to create a map of the projects and their details. The tables are stored in the 'data' directory. 

2. **Dev LLM**: This folder contains the code and pipeline to gather and parse building code information and fine-tube a LLM to be a subject matter expert in these codes. This is experimental and not used in the current version of the product. 

3. **Agenda Extract**: This is the folder aimed to navigate and extract to the agenda items from the city websites. This is experimental and not used in the current version of the product. 


## Getting Started

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/RegionIntelligence/official-repo.git
    ```

2. **Navigate to the Directory**: 
    ```bash
    cd official-repo
    ```

3. **Install Poetry**: The environment is a poetry environment. To install poetry follow the instructions here: https://python-poetry.org/docs/#installation. Each project has a pyproject.toml file that contains the dependencies for the project. Each project has its own virtual environment. Once Poetry is installed you can navigate to the project directory and run the following command to install the dependencies for the project. 
     ```bash
    poetry update 
    ```

## Feedback & Contributions

We value the developer community and welcome contributions, feedback, and issues. 

