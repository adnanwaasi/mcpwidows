from server import mcp 
from utils.file_reader import read_parquet_summary

@mcp.tool()
def summarise_parquet_file(filename):
    return read_parquet_summary(filename)
