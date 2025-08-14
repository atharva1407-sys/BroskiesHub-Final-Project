from utils.db_utils import init_db
import main_ui

if __name__ == "__main__":
    init_db()
    main_ui.run_app()
