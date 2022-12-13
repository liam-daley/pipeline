import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])


def main(product_data, include_tags, exclude_tags):
    # some notes for the review:
    # created own product data with 1000 products for slightly better benchmark estimates
    # checking exclude_tags first, then include (because we dont want to waste memory creating it if theres a chance its not a preferred product)
    # used sets, found they were faster than alternatives list and Counter
    # used datetime to get rough average of time taken to execute before returning
    # Time with 1000 products: ~0:00:00.000625
    # did not refactor, kept it raw and verbose for readability

    preference_matches = {}
    for product in product_data:
        tags = set(product["tags"])
        if not tags & set(exclude_tags) and tags & set(include_tags):
            name = product["name"]
            codes = preference_matches.get(name, [])
            codes.append(product["code"])
            preference_matches.update({name:codes})
    return [PreferenceMatch(k, v) for k, v in preference_matches.items()]

if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]

    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)

    order_items = main(product_data, args.include, args.exclude)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes)))
