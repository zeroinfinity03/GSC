# Graduate Success Center Analytics Dashboard

📊 A Streamlit dashboard for analyzing Graduate Success Center appointment data.

## Features

- **Interactive Visualizations**: Analyze appointments by staff, DSS student distribution, and project types.
- **Date and Staff Filters**: Easily filter data by date range and staff members.
- **Scrollable Layout**: Enhanced layout for better visibility and interaction.
- **Raw Data View**: Option to view the raw data in an expandable section.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/gsc-analytics.git
   cd gsc-analytics
   ```

2. **Install Dependencies**:
   Using `uv`:
   ```bash
   uv pip install -e .
   ```

3. **Run the App**:
   ```bash
   uv run streamlit run app.py
   ```

4. **Access the Dashboard**:
   Open your web browser and go to `http://localhost:8501`.

## Project Structure

- `app.py`: Main Streamlit application.
- `GSC cleaned.csv`: Data file used for analysis.
- `pyproject.toml`: Project dependencies and metadata.
- `README.md`: Project documentation.
- `.venv/`: Virtual environment directory (created by `uv`).

## Dependencies

- `streamlit`
- `plotly`
- `pandas`
- `polars`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For questions or feedback, please contact [yourname@example.com](mailto:yourname@example.com).
