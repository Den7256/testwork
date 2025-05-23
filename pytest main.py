import pytest
from io import StringIO
from main import EmployeeDataProcessor


@pytest.fixture
def sample_csv_data():
    return StringIO(
        "id,email,name,department,hours_worked,salary\n"
        "1,alice@test,Alice,Marketing,160,50\n"
        "2,bob@test,Bob,Design,150,40\n"
    )


def test_payout_report(sample_csv_data, tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text(sample_csv_data.getvalue())

    processor = EmployeeDataProcessor()
    processor.read_csv_files([str(test_file)])
    report = processor.generate_report('payout')

    assert "Alice" in report
    assert "Bob" in report
    assert "$8000" in report  # 160 * 50
    assert "$6000" in report  # 150 * 40