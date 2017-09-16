# -*- coding: utf-8 -*-
import argparse
import csv
import logging
from StringIO import StringIO

from backend import db

log = logging.getLogger(__name__)

BATCH_SIZE_FOR_PRODUCT_INDEX = 500
HEADER_NAMES = ['event_id', 'user_id', 'session_id', 'time', 'session_time', 'library', 'platform', 'device_type',
                'country', 'region', 'city', 'ip', 'referrer', 'landing_page', 'browser', 'search_keyword',
                'utm_source', 'utm_campaign', 'utm_medium', 'utm_term', 'utm_content', 'device', 'carrier', 'app_name',
                'app_version', 'domain', 'query', 'path', 'hash', 'title', 'view_controller', 'screen_a11y_id',
                'screen_a11y_label']


class HeapDataImporter(object):

    def __init__(self):

        self.succeed_count = 0
        self.failed_lines = []

    def import_data(self, file_name):
        log.info("Start to import file:{}".format(file_name))
        self._import_data(file_name)
        log.info("End for importing. succeed count is {}".format(self.succeed_count))
        if self.failed_lines:
            log.error("failed lines: {}".format(self.failed_lines))

    def _import_data(self, file_name):
        if not file_name:
            log.error("file_name mustn't be empty !!!")
            return
        raw_data = self._read_raw_data(file_name)
        self._save_data(raw_data)

    def _read_raw_data(self, file_name):
        """
        read raw data from S3 or File
        """
        with open(file_name) as csv_file:
            raw_data = csv_file.read()

        return StringIO(raw_data)

    def _save_data(self, raw_data):
        conn = db.get_connection()
        cursor = conn.cursor()
        reader = csv.DictReader(raw_data, fieldnames=HEADER_NAMES, delimiter=',')
        next(reader)
        line_no = 1
        for row in reader:
            line_no += 1
            sql = "INSERT INTO user_event (event_id, user_id, session_id, time, session_time, library, "
            "platform, device_type, country, region, city, ip, referrer, landing_page, browser, domain, "
            "query, path, title) "
            "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (row['event_id'],
                                                                                                      row['user_id'],
                                                                                                      row['session_id'],
                                                                                                      row['time'],
                                                                                                      row['session_time'],
                                                                                                      row['library'],
                                                                                                      row['platform'],
                                                                                                      row['device_type'],
                                                                                                      row['country'],
                                                                                                      row['region'],
                                                                                                      row['city'],
                                                                                                      row['ip'],
                                                                                                      row['referrer'],
                                                                                                      row['landing_page'],
                                                                                                      row['browser'],
                                                                                                      row['domain'],
                                                                                                      row['query'],
                                                                                                      row['path'],
                                                                                                      row['title'])
            cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def _purge_value(self, raw_value):
        """purge string value"""
        if raw_value is None:
            return raw_value

        return raw_value.replace(u'\xa0', u' ').strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-path', '-f', dest='file-path', help='file-path')
    args = parser.parse_args()
    HeapDataImporter().import_data(args.__dict__['file-path'])
