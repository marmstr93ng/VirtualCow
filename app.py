import logging
import logging.config


def main():
    """Function that defines the workflow of the tool"""

    logging.config.fileConfig('logging/log_settings.conf')
    logging.info("Beginning Script")

if __name__ == '__main__':

    main()
