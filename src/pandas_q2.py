'''
    Author: University of Illinois at Urbana Champaign
    DateTime: 2023-11-05 10:42:47
    FilePath: src/pandas_q2.py
    Description:
'''

import pandas as pd

from difference import Difference
from report import get_file, report


@report
def pandas_q2(data_file: str, pattern_file: str) -> str:
    # TODO: begin of your codes
    data_df = pd.read_csv(data_file, sep=" ", header=None, names=["src", "dest", "src_label", "dest_label", "edge_label"])
    pattern_df = pd.read_csv(pattern_file, sep=" ", header=None, names=["src", "dest", "src_label", "dest_label", "edge_label"])

    unique_nodes = pd.concat([pattern_df["src"], pattern_df["dest"]]).unique()
    unique_nodes.sort() 


    relations = []
    for i, row in pattern_df.iterrows():
        relation = data_df[
            (data_df["src_label"] == row["src_label"]) &
            (data_df["dest_label"] == row["dest_label"]) &
            (data_df["edge_label"] == row["edge_label"])
        ][["src", "dest"]].rename(columns={"src": f"u{row['src']}", "dest": f"u{row['dest']}"})
        relations.append(relation)

    results = relations[0]
    for relation in relations[1:]:
        common_columns = list(set(results.columns) & set(relation.columns))
        results = results.merge(relation, on=common_columns)
    expected_columns = [f"u{node}" for node in unique_nodes]
    results = results[expected_columns]
    results = results.sort_values(by=expected_columns).reset_index(drop=True)

    output_path = "pandas_q2.csv"
    results.to_csv(output_path, index=False, header=False)

    return output_path
    # TODO: end of your codes


def test(data, pattern, expect) -> int:
    # import the logger to output message
    import logging
    logger = logging.getLogger()
    data = get_file('data', data)
    pattern = get_file('pattern', pattern)
    expect = get_file('expect', expect)


    # run the test
    print("**************begin pandas_q2 test**************")
    diff = Difference(pandas_q2(data, pattern), expect)
    try:
        assert(diff.match)
        print('*******************pass*******************')
        return 20
    except Exception as e:
        logger.error("Exception Occurred:" + str(e))
        print('*******************fail*******************')
        print(diff.actual)
        print(diff.expect)
        return 0


if __name__ == "__main__":
    data = 'data/1.txt'
    pattern = 'pattern/2.txt'
    expect = 'expect/d1-p2.txt'
    test(data, pattern, expect)
