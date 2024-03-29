import argparse
from pprint import pprint
import json
import os
import time

##Base Gladier imports
from gladier import GladierBaseClient, generate_flow_definition

##Import tools that will be used on the flow definition
from tools.uplink_transfer import UplinkTransfer
from tools.run_laue import QSubLaunch
from tools.downlink_transfer import DownlinkTransfer
from tools.downlink_index import DownlinkIndex

##Generate flow based on the collection of `gladier_tools`
# In this case `SimpleTransfer` was defined and imported from tools.uplink
@generate_flow_definition
class LaueClient(GladierBaseClient):
    gladier_tools = [
        UplinkTransfer,
        QSubLaunch,
        DownlinkTransfer,
        DownlinkIndex
    ]

##  Arguments for the execution of this file as a stand-alone client
def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment_name', help='Unique point ID')
    parser.add_argument('point_path', help='Unique point ID')
    return parser.parse_args()

def wait_callback(*args, **kwargs):
    time.sleep(60)

## Main execution of this "file" as a Standalone client
if __name__ == '__main__':
    scan_name = 'test_exp'

    args = arg_parse()

    with open('laue_conf.json') as conf_f:
        conf = json.load(conf_f)

    with open('uids.json') as uids_f:
        uids = json.load(uids_f)

    ##The first step Client instance
    exampleClient = LaueClient()


    point_file = os.path.basename(args.point_path)

    ## Flow inputs necessary for each tool on the flow definition.
    results_folder = f'intermediate/{args.experiment_name}/{scan_name}/results/'
    scan_folder = f'intermediate/{args.experiment_name}/{scan_name}/scans/'
    repacks_folder = f'{args.experiment_name}/{scan_name}/repacks/'
    index_folder = f'{args.experiment_name}/{scan_name}/indexes/'
    point_folder = point_file.split('.')[0]
    flow_input = {
        'input': {
            # To Eagle
            'uplink_source_endpoint_id': conf['voyager']['uuid'],
            'uplink_source_path': os.path.join(conf['voyager']['dm_experiment'], args.experiment_name, point_file),
            'uplink_destination_endpoint_id': conf['eagle_34ide']['uuid'],
            'uplink_destination_path': os.path.join(conf['eagle_34ide']['staging'], scan_folder, point_file),

            # QSub Launch
            'im_dir': os.path.join(conf['eagle_34ide']['absolute'], scan_folder, point_file),
            'out_dir': os.path.join(conf['eagle_34ide']['absolute'], results_folder, point_folder),
            'repack_dir': os.path.join(conf['eagle_34ide']['absolute'], repacks_folder, point_folder),
            'index_dir': os.path.join(conf['eagle_34ide']['absolute'], index_folder, point_folder),
            'funcx_endpoint_compute': uids['endpoint'],

            # From Eagle
            'downlink_source_endpoint_id': conf['eagle_34ide']['uuid'],
            'downlink_source_path': os.path.join(conf['eagle_34ide']['staging'], repacks_folder, point_folder),
            'downlink_destination_endpoint_id': conf['clutch']['uuid'],
            'downlink_destination_path': os.path.join(conf['clutch']['staging'], 'polaris_results', scan_name, 'recons', point_folder),

            'downlink_index_source_path': os.path.join(conf['eagle_34ide']['staging'], index_folder, point_folder),
            'downlink_index_destination_path': os.path.join(conf['clutch']['staging'], 'polaris_results', scan_name, 'indexes', point_folder),
        }
    }
    print('Created payload.')
    pprint(flow_input)
    print('')
    ##Label for the current run (This is the label that will be presented on the globus webApp)
    client_run_label = 'Laue Cold Processing'

    #Flow execution
    flow_run = exampleClient.run_flow(flow_input=flow_input, label=client_run_label)

    # Wait and don't overload query limit
    #exampleClient.progress(flow_run['action_id'], callback=wait_callback)

    print('Run started with ID: ' + flow_run['action_id'])
    print('https://app.globus.org/runs/' + flow_run['action_id'])
