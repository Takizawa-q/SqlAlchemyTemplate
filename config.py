from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class DB:
    """Database configuration with connection parameters."""
    user: str
    password: str
    database: str
    host: str
    port: int


@dataclass
class Redis:
    """Redis configuration with connection parameters."""
    password: Optional[str]
    port: int
    host: str
    use_redis: bool

    def data_source_name(self) -> str:
        """Generate Redis connection string."""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/0"
        return f"redis://{self.host}:{self.port}/0"


@dataclass
class TgBot:
    """Telegram bot configuration."""
    token: str
    admins: list[int]


@dataclass
class Application:
    debug: bool


@dataclass
class Config:
    """Main application configuration."""
    tg_bot: Optional[TgBot]
    db: Optional[DB]
    redis: Optional[Redis]
    app: Application


def load_config() -> Config:
    """Load configuration from environment variables."""
    try:
        env = Env()
        env.read_env()

        use_db = env.bool("USE_DB", default=False)
        use_tgbot = env.bool("USE_TGBOT", default=False)

        db_config = None
        if use_db:
            user = env.str("DB_USER")
            password = env.str("DB_PASSWORD")
            database = env.str("DB_DATABASE")
            host = env.str("DB_HOST")
            port = env.int("DB_PORT")

            db_config = DB(
                user=user,
                password=password,
                database=database,
                host=host,
                port=port,
            )

        tgbot_config = None
        if use_tgbot:
            tgbot_config = TgBot(
                token=env.str("TOKEN"),
                admins=env.list("ADMINS", subcast=int),
            )

        redis_config = None
        if env.bool("USE_REDIS", default=False):
            redis_config = Redis(
                use_redis=True,
                password=env.str("REDIS_PASS", default=None),
                host=env.str("REDIS_HOST"),
                port=env.int("REDIS_PORT")
            )
        app_config = Application(
            debug=env.bool("APP_DEBUG", default=False)
        )
        return Config(
            tg_bot=tgbot_config,
            db=db_config,
            redis=redis_config,
            app=app_config
        )
    except Exception as e:
        raise ValueError(f"Configuration loading failed: {e}")

config = load_config()
# .env file ex
"""
USE_DB=true
USE_TGBOT=true
USE_REDIS=true

# Database configuration
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_DATABASE=your_db_name
DB_HOST=your_db_host
DB_PORT=5432

# Telegram bot configuration
TOKEN=your_telegram_bot_token
ADMINS=123456789,987654321

# Redis configuration
REDIS_PASS=your_redis_password
REDIS_HOST=your_redis_host
REDIS_PORT=6379

# Application configuration
APP_DEBUG=true
"""
