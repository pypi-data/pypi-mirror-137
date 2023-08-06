import datetime

from miroflowexport.internal import miroaccess as mac
from miroflowexport.internal import exporter

class MiroAccess:

    def __init__(self, log, token, board_id):
        self._log = log
        self._token = token
        self._board_id = board_id

    def try_get_task_list(self):
        ###
        # Tries to fetch the list of sticky notes from the Miro board and returns them as tasks with additional information.
        #
        # Returns a tuple (success_as_bool, dict_of_tasks_by_id) with success is either True or False
        ###
        response = mac.send_request_widgets(self._log, token = self._token, board_id = self._board_id)
        self._log.debug("Response is: {}".format(response))
        success = mac.is_response_ok(self._log, response)

        if not success:
            return (False, {})

        tasks = mac.get_list_of_cards(self._log, response.text)
        mac.get_list_of_dependencies(self._log, response.text, tasks)
        return (True, tasks)

    def try_get_all_board_content(self):
        ###
        # Tries to get the complete list of widgets for backup.
        ###
        response = mac.send_request_widgets(self._log, token = self._token, board_id=self._board_id)
        self._log.debug("Response is: {}".format(response))
        success = mac.is_response_ok(self._log, response)

        if not success:
            self._log.error("Cannot fetch board content.")
            return {}

        return response.text

    def export_to_excel(self, tasks_dict, path = "tmp/excel.xlsx"):
        eexp = exporter.ExcelExporter(self._log, path)
        return eexp.export_tasks(tasks_dict)
        
    def export_board_to_excel(self, path = "tmp/excel.xlsx", source_path = None):
        self._log.info("Fetching board content ...")
        (success, tasks_dict) = self.try_get_task_list()
        if not success:
            self._log.error("Fetching board content failed.")
            return False

        date_offset = datetime.date.today()
        if source_path:
            eimp = exporter.ExcelImporter(self._log, source_path)
            success = eimp.import_from_excel()
            if not success:
                self._log.error("Loading existing tasks from {} failed. I will continue without using existing Excel data.".format(source_path))
            else:
                old_tasks_dict = eimp.get_tasks()
                date_offset = eimp.get_date_offset()
                updater = exporter.TaskUpdater(self._log)
                success = updater.update_tasks(tasks_dict, old_tasks_dict)
                if not success:
                    self._log.error("Updating tasks from existing plan {} failed.".format(source_path))
                else:
                    tasks_dict = updater.get_tasks()

        self._log.info("Exporting board content to file {} ...".format(path))
        eexp = exporter.ExcelExporter(self._log, path)
        success = eexp.export_tasks(tasks_dict, date_offset)
        
        if not success:
            self._log.error("Exporting board content to Excel failed.")
            return False

        return True
