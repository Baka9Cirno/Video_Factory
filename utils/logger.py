import logging, os

# Get api logger and llm logger
def get_loggers(log_dir, mode="w"):
    llm_api_log_path = os.path.join(log_dir, "llm_api.log")
    agent_log_path = os.path.join(log_dir, "agent.log")

    llm_api_logger = logging.getLogger('llm_api_logger')  # 命名 Logger
    llm_api_logger.setLevel(logging.INFO)  # 设置 Logger 级别
    llm_api_logger.propagate = False  # 防止日志传播到根 Logger
    llm_api_handler = logging.FileHandler(llm_api_log_path, mode=mode)
    llm_api_handler.setLevel(logging.INFO)
    llm_api_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    llm_api_handler.setFormatter(llm_api_formatter)
    llm_api_logger.addHandler(llm_api_handler)

    agent_logger = logging.getLogger('agent_logger')  # 命名 Logger
    agent_logger.setLevel(logging.INFO)  # 设置 Logger 级别
    agent_logger.propagate = False  # 防止日志传播到根 Logger
    agent_handler = logging.FileHandler(agent_log_path, mode=mode)
    agent_handler.setLevel(logging.INFO)
    agent_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    agent_handler.setFormatter(agent_formatter)
    agent_logger.addHandler(agent_handler)

    return llm_api_logger, agent_logger
