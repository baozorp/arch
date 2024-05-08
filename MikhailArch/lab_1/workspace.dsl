workspace {
name "Система чатов"
    description "Система для обмена сообщениями между пользователями и в групповых чатах"

    !identifiers hierarchical

       model {
        properties { 
            structurizr.groupSeparator "/"
        }

        user = person "Пользователь" {
            description "Пользователь системы чатов"
        }

        chat_system = softwareSystem "Система чатов" {
            description "Система для обмена сообщениями и управления чатами"

            user_service = container "User Service" {
                description "Сервис для авторизации и управления пользователями"
                technology "REST API"
            }

            chat_service = container "Chat Service" {
                description "Сервис для работы с PtP и групповыми чатами"
                technology "REST API"
            }

            group "Слой данных" {

                redis_cache = container "Redis Cache" {
                    description "Кеш Redis для ускорения поиска пользователей"
                    technology "Redis"
                    tags "cache"
                }
                postgres_database = container "PostgreSQL Database" {
                    description "База данных PostgreSQL с пользователями и чатами"
                    technology "PostgreSQL"
                    tags "database"
                }

                mongo_database = container "MongoDB Database" {
                    description "База данных MongoDB с историей сообщений"
                    technology "MongoDB"
                    tags "database"
                }
            }

            user -> user_service "Регистрация и авторизация"
            user -> chat_service "Создание и управление чатами, отправка сообщений"

            chat_service -> redis_cache "Получение последних сообщений"
            user_service -> postgres_database "CRUD операции с пользователями, поиск"
            user_service -> chat_service "Передача данных о пользователе после авторизации"

            chat_service -> postgres_database "CRUD операции с чатами"
            chat_service -> mongo_database "CRUD истории сообщений"
            chat_service -> user_service "Проверка авторизации пользователя при добавлении в чат и отправке сообщений"
        }

        deploymentEnvironment "Production" {
        deploymentNode "Chat Server" {
            containerInstance chat_system.user_service
            containerInstance chat_system.chat_service
            properties {
                "cpu" "4"
                "ram" "256Gb"
                "hdd" "4Tb"
            }
        }

        deploymentNode "databases" {

            deploymentNode "Database Server 1" {
                containerInstance chat_system.postgres_database
                properties {
                    "cpu" "4"
                    "ram" "256Gb"
                    "hdd" "4Tb"
                }
            }

            deploymentNode "Cache Server" {
                containerInstance chat_system.redis_cache
                properties {
                    "cpu" "2"
                    "ram" "128Gb"
                    "hdd" "2Tb"
                }
            }

            deploymentNode "DocumentDB Server" {
                containerInstance chat_system.mongo_database
                instances 4
                properties {
                    "cpu" "4"
                    "ram" "256Gb"
                    "hdd" "4Tb"
                }
            }
        }
    }
}


    views {
        themes default

        properties { 
            structurizr.tooltips true
        }


        !script groovy {
            workspace.views.createDefaultViews()
            workspace.views.views.findAll { it instanceof com.structurizr.view.ModelView }.each { it.enableAutomaticLayout() }
        }

        dynamic chat_system "UC01" "Создание нового пользователя" {
            autoLayout
            user -> chat_system.user_service "Создать нового пользователя (POST /users)"
            chat_system.user_service -> chat_system.postgres_database "Сохранить данные о пользователе"
        }

        dynamic chat_system "UC02" "Поиск пользователя по логину" {
            autoLayout
            user -> chat_system.user_service "Поиск пользователя (GET /users?login={login})"
            chat_system.user_service -> chat_system.postgres_database "Поиск в базе данных"
            chat_system.postgres_database -> chat_system.user_service "Вернуть данные пользователя"
        }

        dynamic chat_system "UC03" "Поиск пользователя по маске имя и фамилии" {
            autoLayout
            user -> chat_system.user_service "Поиск пользователя (GET /users?name={name}&surname={surname})"
            chat_system.user_service -> chat_system.postgres_database "Поиск в базе данных"
            chat_system.postgres_database -> chat_system.user_service "Вернуть данные пользователя"
        }

        dynamic chat_system "UC04" "Создание группового чата" {
            autoLayout
            user -> chat_system.chat_service "Создать групповой чат (POST /group_chats)"
            chat_system.chat_service -> chat_system.user_service "Проверить авторизацию пользователя"
            chat_system.user_service -> chat_system.chat_service "Подтвердить авторизацию"
            chat_system.chat_service -> chat_system.postgres_database "Сохранить данные группового чата"
        }

        dynamic chat_system "UC05" "Добавление пользователя в чат" {
            autoLayout
            user -> chat_system.chat_service "Добавить пользователя в чат (POST /group_chats/{chat_id}/users)"
            chat_system.chat_service -> chat_system.user_service "Проверить авторизацию пользователя"
            chat_system.user_service -> chat_system.chat_service "Подтвердить авторизацию"
            chat_system.chat_service -> chat_system.postgres_database "Добавить пользователя в чат"
        }

        dynamic chat_system "UC06" "Добавление сообщения в групповой чат" {
            autoLayout
            user -> chat_system.chat_service "Добавить сообщение (POST /group_chats/{chat_id}/messages)"
            chat_system.chat_service -> chat_system.user_service "Проверить авторизацию пользователя"
            chat_system.user_service -> chat_system.chat_service "Подтвердить авторизацию"
            chat_system.chat_service -> chat_system.redis_cache "Сохранить последнее сообщение в кэш"
            chat_system.chat_service -> chat_system.mongo_database "Сохранить сообщение в истории"
        }

        dynamic chat_system "UC07" "Загрузка сообщений группового чата" {
            autoLayout
            user -> chat_system.chat_service "Загрузить сообщения (GET /group_chats/{chat_id}/messages)"
            chat_system.chat_service -> chat_system.user_service "Проверить авторизацию пользователя"
            chat_system.user_service -> chat_system.chat_service "Подтвердить авторизацию"
            chat_system.chat_service -> chat_system.redis_cache "Проверить наличие последних сообщений в кэше"
            chat_system.redis_cache -> chat_system.chat_service "Вернуть последние сообщения (если есть)"
            chat_system.chat_service -> chat_system.mongo_database "Получить историю сообщений (если нет в кэше)"
            chat_system.mongo_database -> chat_system.chat_service "Вернуть последние сообщения"
        }

        dynamic chat_system "UC08" "Отправка PtP сообщения пользователю" {
            autoLayout
            user -> chat_system.chat_service "Отправить PtP сообщение (POST /ptp/{user_id}/messages)"
            chat_system.chat_service -> chat_system.user_service "Проверить авторизацию пользователя"
            chat_system.user_service -> chat_system.chat_service "Подтвердить авторизацию"
            chat_system.chat_service -> chat_system.redis_cache "Сохранить последнее PtP сообщение в кэш"
            chat_system.chat_service -> chat_system.mongo_database "Сохранить PtP сообщение в истории"
        }

        dynamic chat_system "UC09" "Получение PtP списка сообщений для пользователя" {
            autoLayout
            user -> chat_system.chat_service "Получить список PtP сообщений (GET /ptp/{user_id}/messages)"
            chat_system.chat_service -> chat_system.redis_cache "Проверить наличие последних PtP сообщений в кэше"
            chat_system.redis_cache -> chat_system.chat_service "Вернуть последние PtP сообщения (если есть)"
            chat_system.chat_service -> chat_system.mongo_database "Запросить историю PtP сообщений (если нет в кэше)"
            chat_system.mongo_database -> chat_system.chat_service "Вернуть список сообщений"
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}
