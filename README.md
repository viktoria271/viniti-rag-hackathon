# ВИНИТИ RAG: пайплайн извлечения

## Запуск на ПК (Windows / Linux)
1. `git pull`
2. `python -m pip install -r requirements.txt -r tools/requirements.txt`
3. Скопируй `.env.example` в `.env`, впиши `GEMINI_API_KEY=<ключ>`.
4. Положи PDF в `dev/` (D001–D021).
5. Пробный прогон: `python main.py --input dev --output out_dev --only D001 D002`
6. Весь набор: `python main.py --input dev --output out_dev`
   (кэш в `cache/`; `--force` — перезапрос; `--rebuild-csv-only` — пересобрать CSV без API).
7. Проверка формата: `python tools/check_submission.py out_dev dev --json-report report.json`
8. Оценка по эталону: `python scripts/evaluate.py out_dev dev_gold`
9. Пришли разработчику вывод шагов 7 и 8.
