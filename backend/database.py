python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение строки подключения из переменных окружения
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:secret@localhost:5432/os_management"
)

# Создание движка SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    echo=False  # В продакшене установите False, для отладки - True
)

# Создание фабрики сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии БД (используется в зависимостях FastAPI)
def get_db():
    """
    Генератор сессии БД.
    Гарантирует закрытие сессии после использования.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для инициализации БД (создание таблиц)
def init_db():
    """
    Создает все таблицы в базе данных на основе моделей.
    Вызывается при первом запуске приложения.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ База данных инициализирована")

# Тестовое подключение к БД
def test_connection():
    """
    Проверяет подключение к базе данных.
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Подключение к базе данных успешно")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False

# Если файл запущен напрямую
if __name__ == "__main__":
    if test_connection():
        init_db()
