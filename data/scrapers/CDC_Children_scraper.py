# run 'scrapy runspider CDC_Children_scraper.py' to scrape data

from datetime import date
import scrapy
import pandas as pd

class CovidScraper(scrapy.Spider):
  name = "CDC_Children_Scraper"
  start_urls = ["https://www.cdc.gov/coronavirus/2019-ncov/prepare/children-faq.html"]

  def parse(self, response):
    columns = {
      "question" : [],
      "answer" : [],
      "answer_html" : [],
      "link" : [],
      "name" : [],
      "source" : [],
      "category" : [],
      "country" : [],
      "region" : [],
      "city" : [],
      "lang" : [],
      "last_update" : [],
    }

    found_p = False
    found_question = False
    current_answer = ""

    all_nodes = response.xpath("//*")
    for node, next_node in zip(all_nodes, all_nodes[1:]):
      # iterate until end of question-answer block
      if node.attrib.get("class") != "row d-none d-lg-block":
        # check if question (<p><strong>QUESTION</strong></p>)
        if node.xpath("name()").get() == "p":
          found_p = True

        # in new question
        if found_p and (node.xpath("name()").get() == "strong"):
          # save previous question
          if current_answer:
            columns["question"].append(current_question)
            columns["answer"].append(current_answer)
            columns["answer_html"].append(current_answer_html)

          # process new question
          current_question = node.css("::text").get()
          current_question = current_question.split("Q:", maxsplit=1)[-1].strip()
          found_question = True
          current_answer = ""
          current_answer_html = ""
          continue

        # construct answer
        if found_question and (node.xpath("name()").get() != "a") and (next_node.xpath("name()").get() != "strong"):
          #print(node)
          answer_part = node.css("::text").getall()
          current_answer += " ".join(answer_part).strip()
          answer_part_html = node.getall()
          current_answer_html += " ".join(answer_part_html).strip()

      else:
        columns["question"].append(current_question)
        columns["answer"].append(current_answer)
        columns["answer_html"].append(current_answer_html)
        break

    today = date.today()

    columns["link"] = ["https://www.cdc.gov/coronavirus/2019-ncov/prepare/children-faq.html"] * len(columns["question"])
    columns["name"] = ["Coronavirus Disease-2019 (COVID-19) and Children"] * len(columns["question"])
    columns["source"] = ["Center for Disease Control and Prevention (CDC)"] * len(columns["question"])
    columns["category"] = ["Children"] * len(columns["question"])
    columns["country"] = ["USA"] * len(columns["question"])
    columns["region"] = [""] * len(columns["question"])
    columns["city"] = [""] * len(columns["question"])
    columns["lang"] = ["en"] * len(columns["question"])
    columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

    return columns
