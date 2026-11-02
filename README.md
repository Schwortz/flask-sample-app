# Flask Sample App with Tests

This is a simple Flask web application with unit tests. The application provides a basic REST API for managing a list of items. It serves as a starting point for learning how to create a Flask application and write tests for it.

## Project Structure

The project is organized as follows:

- `app/`: Contains the Flask application and routes.
- `tests/`: Houses unit tests for the application.
- `run.py`: A script to run the Flask application.

## Getting Started

To get the Flask app up and running on your local machine, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd flask_sample_app
   ```

2. **Set Up a Virtual Environment:**

   It's recommended to create a virtual environment to isolate project dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies:**

   Install the necessary dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   Start the Flask application:

   ```bash
   python run.py
   ```

   The app will be available at [http://localhost:5001](http://localhost:5001). The default port is 5001; set the `PORT` environment variable to override it (e.g. `PORT=8000 python run.py`).

5. **Run Tests:**

   To run the unit tests, execute the following command:

   ```bash
   python -m unittest discover tests
   ```

   This command will discover and run all tests in the `tests` directory.

## Application Routes

The application keeps items in memory (they are lost on restart). Route functions in `app/routes.py` are type-annotated.

| Route | Method | Status codes | Description |
|-------|--------|--------------|-------------|
| `/` | GET | 200 | Returns the plain-text greeting `Hello, Flask!`. |
| `/items` | GET | 200 | Returns all items. |
| `/items/<item_id>` | GET | 200, 404 | Returns the item at the zero-based integer index `item_id`, or an error if it does not exist. |
| `/items` | POST | 201 | Adds the JSON request body as a new item. |

Example bodies:

```bash
# POST /items  -> 201
curl -X POST http://localhost:5001/items -H "Content-Type: application/json" -d '{"name": "apple"}'
# {"message": "Item added successfully"}

# GET /items  -> 200
# {"items": [{"name": "apple"}]}

# GET /items/0  -> 200
# {"item": {"name": "apple"}}

# GET /items/5  -> 404
# {"error": "Item not found"}
```

### Type checking

Static types can be checked with [mypy](https://mypy-lang.org/), which is an optional dev tool and not in `requirements.txt`:

```bash
pip install mypy
mypy app/routes.py
```

## Testing

Unit tests are provided in the `tests` directory. They cover the basic functionality of the application, including route handling and response validation. You can use these tests as a reference to write your own tests or to verify the correctness of the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribute

Feel free to contribute to this project by opening issues or submitting pull requests. We welcome any improvements, bug fixes, or additional features.

## Author

- Pan Luo

## Acknowledgments

- This project was created as a sample Flask application for educational purposes.
- Special thanks to the Flask community for providing a fantastic web framework.

Enjoy experimenting with the Flask sample app! If you have any questions or need further assistance, please don't hesitate to reach out.
