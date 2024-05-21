# Animal Video Classifier Web Application

This project is a web application that allows users to upload videos, which are then scanned and classified based on the types of animals detected. The application is containerized for easy deployment and management, and includes a CLI for database operations, as well as sample images and a sample client for testing purposes.

## Project Structure

- **containers/**: Contains the Docker info to run iterations of the application.
- **cli/**: Contains the command-line interface tools for managing the database.
- **sampleClient/**: Contains a sample client for testing api endpoints.

## Features

- **Video Upload**: Upload videos to the web application for analysis.
- **Animal Detection**: Automatically scans and classifies animals in the uploaded videos.
- **Containerized**: The application is containerized using Docker for easy deployment.
- **CLI Tools**: Manage the database using command-line interface tools.

## Getting Started

### Prerequisites

- Docker installed on your machine.
- Python installed on your machine (for CLI tools).
- Dotnet installed on your machine (for sampleClient).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/animal-video-classifier.git
   cd animal-video-classifier
    ```
2. **Build the Docker containers:**
   ```bash
   cd containers/PytorchWildlife
   docker-compose up -d
   ```