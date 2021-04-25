import pandas as pd
import util.general_util as gu


# Create new table
if __name__ == "__main__":
    sqlEngine = gu.create_sqlite_engine()
    df = pd.DataFrame(columns=['links', 'extracted_entity', 'entity_details'])
    df.to_sql("extracted_entities", con=sqlEngine, index=False)

