# Pokedex Project

This project is a Pokedex application that allows users to search for Pokémon cards, view card details, and manage their collections. The project is split into a backend and frontend, leveraging Python and React.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Backend

1. Clone the repository:
    ```bash
    git clone https://github.com/redfred91/pokedex-app.git
    ```
2. Navigate to the backend directory:
    ```bash
    cd pokedex-app/python-backend/pokedexBackend
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Frontend

1. Navigate to the frontend directory:
    ```bash
    cd pokedex-app/react-app
    ```
2. Install the required dependencies:
    ```bash
    npm install
    ```

## Usage

### Backend

1. Start the backend server:
    ```bash
    python3 app.py
    ```

### Frontend

1. Start the frontend development server:
    ```bash
    npm start
    ```

### Running the Full Application

1. Ensure the backend server is running:
    ```bash
    cd pokedex-app/python-backend/pokedexBackend
    python3 app.py
    ```
2. In a new terminal, start the frontend development server:
    ```bash
    cd pokedex-app/react-app
    npm start
    ```

The application will be accessible at `http://localhost:3000`.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
