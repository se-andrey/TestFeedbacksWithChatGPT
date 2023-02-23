from settings import API_KEY
import openai
import csv

openai.api_key = API_KEY


def get_response(request_chatgpt: str, data_processing: str):
    """
    Using ChatGPT to process data
    :param request_chatgpt: "str"
    how ChatGPT should process the data,
    :param data_processing: "str"
    what data needs to be processed
    :return: "list"
    list of answers
    """
    try:
        my_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{request_chatgpt} \n{data_processing}",
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        return my_response["choices"][0]["text"].strip().split(", ")
    except Exception as ex:
        return f"{ex}"


def get_data(name: str):
    """
    Read data from .csv and return string like "name: data \n name: data ..."
    :param name: str
    :return: str
    """
    try:
        with open(name, encoding="utf-8") as file:
            data = csv.reader(file, delimiter=",")
            result = []
            for string in data:
                # combining column elements into rows like "name: data"
                result.append(": ".join(string))
            data = "\n".join(result)
            return data
    except FileNotFoundError as ex:
        print(f"{ex}. Please enter correctly file")
    except Exception as ex:
        print(ex)


def save_result(file_name: str, request_chatgpt: list):
    """
    Read the file by line, add the result of the request to ChatGPT
    and write it to a new file filename + "analyzed.csv"
    :param file_name: str
    :param request_chatgpt: list
    :return: file filename + "analyzed.csv"
    """
    try:
        new_file_name = file_name[:-4] + "_analyzed.csv"
        with open(new_file_name, "w", encoding="utf-8", newline="") as file_to_write:
            try:
                with open(file_name, encoding="utf8") as file_to_read:
                    data = csv.reader(file_to_read, delimiter=",")
                    for string in data:
                        string = list(string)
                        # cycle on answers
                        for i in range(len(request_chatgpt)):
                            # check name (email) in answers
                            if string[0] in request_chatgpt[i]:
                                # select the result
                                result = request_chatgpt[i].replace(string[0] + ": ", "").strip()
                                del request_chatgpt[i]
                                break
                        # string + result for write in csv file
                        string.append(result)
                        file_write = csv.writer(file_to_write)
                        file_write.writerow(string)
            except Exception as ex:
                print(ex)
        return new_file_name
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    # specify what we need from ChatGPT
    request_to_chatgpt = """
    Below are reviews of the Alice smart column. Rate each on a ten-point scale, 
    where 1 point is the most negative, and 10 points are the most enthusiastic. 
    Return the result as a sorted list of email addresses - the most enthusiastic is at the top, 
    then according to the rating. Next to each element, specify the rating you received 
    """

    filename = "feedbacks.csv"
    print(f"[*] write you '{filename}' and ask ChatGPT about \n'{request_to_chatgpt[:45].strip()}...'\n In process...")
    data_for_processing = get_data(filename)
    response = get_response(request_to_chatgpt, data_for_processing)
    all_good = save_result(filename, response)
    print(f"[+] check your {all_good}")
