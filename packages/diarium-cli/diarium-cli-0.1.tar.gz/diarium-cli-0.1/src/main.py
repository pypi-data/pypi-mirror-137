from __future__ import annotations
import os
import rich
import click
from click_shell import shell
from src.journal import Journal

journal = Journal()
console = rich.console.Console()


@shell(prompt="Diarium-CLI >> ")
def cli():
    console.print("Type 'help' to show commands")


@cli.command()
@click.option("-w", "--word", required=True, help="Word to search for.")
@click.option("-e", "--exact", is_flag=True, help="Search for exact matches.")
def find(word: str, exact: bool = False):
    """Searches for a <word>."""
    journal.find_word(word=word, exact_match=exact)


@cli.command()
@click.option("-w", "--words", default=10, help="Number of top words showed.")
def stats(words: int):
    """Shows stats."""
    console.print("Entries:", len(journal.entries_map))
    console.print("Words:", journal.get_total_word_count())
    console.print("Unique words:", journal.get_unique_word_count())
    console.print(journal.get_most_frequent_words(words))


@cli.command()
@click.option("-w", "--word", required=True, help="Word to search for.")
def count(word: str):
    """Shows the number of occurrences of a <word>."""
    journal.get_word_count(word)


@cli.command()
@click.option("-d", "--date", required=True, help="Format: dd.mm.yyyy")
def day(date: str):
    """Shows a specific entry."""
    file_content = journal.get_entry_from_date(date=date)
    if file_content is None:
        console.print("File not found")
    else:
        console.print(file_content)


@cli.command()
def random():
    """Shows a random entry."""
    console.print(journal.get_random_day())


@cli.command()
def longest():
    """Shows the longest entry."""
    console.print(journal.get_longest_day())


@cli.command()
def lang():
    """Shows the percentage of English words."""
    eng_word_count = journal.get_english_word_count()
    console.print(f"All words: {journal.get_total_word_count()} | English words: {eng_word_count}")
    console.print(
        f"Percentage of english words: {round(eng_word_count * 100 / journal.get_total_word_count(), 3)}%")


@cli.command()
def folder():
    """Puts entries into files into appropriate folders."""
    journal.create_tree_folder_structure()


@cli.command()
def clear():
    """Clears console."""
    os.system("cls||clear")


if __name__ == "__main__":
    cli()
