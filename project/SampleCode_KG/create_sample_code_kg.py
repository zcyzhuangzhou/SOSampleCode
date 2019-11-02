import json
from pathlib import Path
from definitions import GRAPH_DATA_DIR, REMOVE_DUPLICATE_SAMPLE_CODE
from sekg.graph.accessor import GraphAccessor
from sekg.graph.exporter.graph_data import Neo4jImporter, GraphData
from definitions import GRAPH_FACTORY


def kg_impoter(path):
    graph_client = GRAPH_FACTORY.create_py2neo_graph_by_server_name(server_name="SOSampleCodeKG")
    accessor = GraphAccessor(graph_client)
    importer = Neo4jImporter(accessor)

    # graph_data_path = str(Path(GRAPH_DATA_DIR) / 'jdk8.v5.graph')
    graph_data: GraphData = GraphData.load(path)
    importer.import_all_graph_data(graph_data)


def create_sample_code_kg(graph_data):
    output_graph_data_path = str(Path(GRAPH_DATA_DIR) / 'jdk8_sample_code.v1.graph')
    # # 建索引
    # graph_data.create_index_on_property("Code", "Description")

    with open(REMOVE_DUPLICATE_SAMPLE_CODE) as f:
        api_sample_codes = json.load(f)
    f.close()

    count = 0
    print(len(api_sample_codes))

    for api_sample_code in api_sample_codes:
        count = count + 1
        api_node = graph_data.find_one_node_by_property(property_name="id", property_value=api_sample_code["Id"])
        if api_node is not None:
            api_node_id = api_node["id"]
            code_node_id = graph_data.add_node(node_labels=["sample code"],
                                               node_properties={"Code": api_sample_code["Code"]},
                                               primary_property_name="Code")
            description_node_id = graph_data.add_node(node_labels=["sample code description"],
                                                      node_properties={"Description": api_sample_code["Description"]},
                                                      primary_property_name="Description")
            # api_node_id = graph_data.find_one_node_by_property(property_name="qualified_name",
            #                                                    property_value=api_sample_code["API"])["properties"][
            #     "id"]
            # code_node_id = graph_data.find_one_node_by_property(property_name="Code", property_value=api_sample_code["Code"])["_node_id"]
            # description_node_id = graph_data.find_one_node_by_property(property_name="Description", property_value=api_sample_code["Description"])["_node_id"]
            graph_data.add_relation(startId=api_node_id,
                                    relationType="has sample code",
                                    endId=code_node_id)
            graph_data.add_relation(startId=code_node_id,
                                    relationType="has description",
                                    endId=description_node_id)
        else:
            print(api_sample_code["Id"])

    graph_data.save(output_graph_data_path)


if __name__ == "__main__":
    # graph_data_path = str(Path(GRAPH_DATA_DIR) / 'jdk8_sample_code.v1.graph')
    # kg_impoter(graph_data_path)
    graph_data = GraphData.load(str(Path(GRAPH_DATA_DIR) / 'jdk8_sample_code.v1.graph'))
    # # ids = (489,)
    # # results = graph_data.find_one_node_by_property(property_name="id", property_value=1869)
    # # print(results["id"])
    graph_data.print_graph_info()
    # create_sample_code_kg(graph_data)
