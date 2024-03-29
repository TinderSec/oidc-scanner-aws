import logging

def build_logger():
    log_format = logging.Formatter('%(levelname)s: %(message)s')
    logger = logging.getLogger('Audit Log')
    logger.setLevel(logging.INFO)

    channel = logging.StreamHandler()
    channel.setFormatter(log_format)

    log_file = logging.FileHandler('scan.log')
    log_file.setLevel(logging.INFO)

    logger.addHandler(channel)
    logger.addHandler(log_file)
    return logger

AuditLogger = build_logger()