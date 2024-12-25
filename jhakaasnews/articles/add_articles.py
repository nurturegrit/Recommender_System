import csv

from django.core.exceptions import ObjectDoesNotExist

from .models import Article


def transfer_data_to_article(csv_file_path):
  """
  Transfers data from a CSV file to the Article model.

  Args:
      csv_file_path (str): Path to the CSV file.
  """
  with open(csv_file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      title = row['title']
      content = row['content']
      labels = row.get('labels', '')  # Get labels if present, otherwise empty string

      # Check if article already exists by title
      try:
        existing_article = Article.objects.get(title=title)
        print(f"Article '{title}' already exists, skipping.")
      except ObjectDoesNotExist:
        # Create new Article object
        article = Article(
          title=title,
          content=content,
          labels=labels,
        )
        article.save()
        print(f"Article '{title}' created successfully.")


# Example usage
csv_file_path = "path/to/your/data.csv"
transfer_data_to_article(csv_file_path)