import argparse
from typing import List, Dict, Any, Optional
from collections import defaultdict
import sys


class EmployeeDataProcessor:
    """Обработка данных сотрудников и формирование отчетов."""

    def __init__(self):
        self.employees: List[Dict[str, Any]] = []
        self.report_handlers = {
            'payout': self._generate_payout_report
        }

    def read_csv_files(self, file_paths: List[str]) -> None:
        """Чтение данных из CSV-файлов."""
        for path in file_paths:
            with open(path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
                if not lines:
                    continue
                headers = lines[0].split(',')
                for line in lines[1:]:
                    values = line.split(',')
                    employee = {header.strip(): value.strip() for header, value in zip(headers, values)}
                    self._normalize_employee_data(employee)
                    self.employees.append(employee)

    def _normalize_employee_data(self, employee: Dict[str, str]) -> None:
        """Нормализация названий колонок."""
        rate_keys = {'hourly_rate', 'rate', 'salary'}
        hours_keys = {'hours_worked', 'hours'}

        # Поиск и переименование колонки ставки
        for key in rate_keys:
            if key in employee:
                employee['rate'] = float(employee[key])
                break

        # Поиск и переименование колонки часов
        for key in hours_keys:
            if key in employee:
                employee['hours'] = float(employee[key])
                break

    def _generate_payout_report(self) -> str:
        """Формирование отчета по выплатам."""
        departments = defaultdict(list)
        for emp in self.employees:
            departments[emp['department']].append(emp)

        report = [
            "       name              hours   rate    payout    ",
        ]
        total_hours, total_payout = 0.0, 0.0

        for dept in sorted(departments):
            dept_total_h = 0.0
            dept_total_p = 0.0
            report.append(f"{dept:10}")
            report.append(" ")

            for emp in sorted(departments[dept], key=lambda x: x['name']):
                hours = emp['hours']
                rate = emp['rate']
                payout = hours * rate
                report.append(f"----  {emp['name']:15}     {hours:<5.0f}   {rate:<5.0f}   ${payout:<7.0f}")
                dept_total_h += hours
                dept_total_p += payout

            report.append(f"  {'':10}   {'':15}   {dept_total_h:<5.0f}    ${dept_total_p:<7.0f}  ")
            total_hours += dept_total_h
            total_payout += dept_total_p

        report.append(f"  {'':10}   {'':15}   {total_hours:<5.0f}    ${total_payout:<7.0f}  ")

        return '\n'.join(report)

    def generate_report(self, report_type: str) -> Optional[str]:
        """Генерация отчета заданного типа."""
        handler = self.report_handlers.get(report_type)
        return handler() if handler else None


def main():
    parser = argparse.ArgumentParser(description='Генератор отчетов по сотрудникам.')
    parser.add_argument('files', nargs='+', help='Пути к CSV-файлам')
    parser.add_argument('--report', required=True, help='Тип отчета (например, payout)')
    args = parser.parse_args()

    processor = EmployeeDataProcessor()
    processor.read_csv_files(args.files)
    report = processor.generate_report(args.report)

    if not report:
        print(f"Ошибка: Неизвестный тип отчета '{args.report}'", file=sys.stderr)
        sys.exit(1)
    print(report)


if __name__ == '__main__':
    main()