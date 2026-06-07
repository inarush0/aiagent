import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_contents = os.listdir(target_dir)
        results_list: list[str] = []
        for dir in dir_contents:
            path_to_file = "/".join([target_dir, dir])
            is_dir = os.path.isdir(path_to_file)
            file_size = os.path.getsize(path_to_file)
            results_list.append(f"- {dir}: file_size={file_size}, is_dir={is_dir}")

        return "\n".join(results_list)

    except Exception as e:
        return f"Error: {e}"
