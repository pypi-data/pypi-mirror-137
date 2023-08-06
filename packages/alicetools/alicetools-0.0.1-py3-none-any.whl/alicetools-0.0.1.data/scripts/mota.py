import numpy as np
from tqdm import tqdm
from allensdk.core.reference_space_cache import ReferenceSpaceCache
import pandas as pd
import argparse
from pathlib import Path
import os
from skimage.io import imread

def parse_arguments():
    """
    Function to parse argument from the terminal.
    Returns
    -------
    args: parsed arguments
    """
    # Parse argument for command line use.
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_csv', type=str,
                        help="Path to the CSV file containing the objects.",
                        required=True)
    parser.add_argument('-a', '--atlas', type=str,
                        help="Path to the atlas in same orientation as the segmented data.",
                        required=True)
    parser.add_argument('-z', '--z_downsample', type=float,
                        help="Downsample in Z between original data and atlas",
                        required=True)
    parser.add_argument('-y', '--y_downsample', type=float,
                        help="Downsample in Y between original data and atlas",
                        required=True)
    parser.add_argument('-x', '--x_downsample', type=float,
                        help="Downsample in X between original data and atlas",
                        required=True)
    parser.add_argument('-o', '--output_path', type=str, default='processed',
                        help="Folder path to save the outputs")
    parser.add_argument('-n', '--number_of_parents', type=int,
                        default=0, help='Number of parents to recursively group Allen area.')

    return parser.parse_args()


def get_labels(args):
    """
    Function to get the label for ambiguous (when the label ID is not an integer) objects.

    Parameters
    ----------
    args: (dict) parsed argument from the terminal.

    Returns
    -------
    correct_labels: label corrected by finding the nearest neighbor with an integer ID.
    """
    # Load data
    objects_data = pd.read_csv(args.data_csv)

    # Fetch data to arrays
    n_tot = len(objects_data.index)
    objects_coord = objects_data[['Z', 'Y', 'X']].to_numpy()

    # Map object to Atlas
    atlas = imread(args.atlas)
    objects_coord[:, 0] /= args.z_downsample
    objects_coord[:, 1] /= args.y_downsample
    objects_coord[:, 2] /= args.x_downsample
    objects_coord = np.round(objects_coord).astype("uint64")
    # ind = np.ravel_multi_index(np.round(objects_coord.T/100).astype(int), dims=atlas.shape)
    # objects_id = atlas[ind]
    # TODO: replace this ugly loop with something more efficient (as above).
    correct_labels = np.zeros(n_tot)
    cnt = 0
    for i in tqdm(range(n_tot), desc='Mapping objects...'):
        try:
            correct_labels[i] = atlas[objects_coord[i, 0], objects_coord[i, 1], objects_coord[i, 2]]
        except IndexError:
            cnt += 1

    if cnt > 0:
        print('Warning: {} objects where outside of the data range. Please check that the downsampling factor is '
              'correct and that it corresponds to the unit in the CSV file.'.format(cnt))

    return correct_labels


def get_mapping(labels, n):
    """
    Get the mapping between area ID and name with Allen SDK.

    Parameters
    ----------
    labels: (array) array of labels to group by ID and fetch area name.
    n: (int) number of parent area to group for.

    Returns
    -------
    area_count: (dict) area names with the counts.
    """
    rspc = ReferenceSpaceCache(25, 'annotation/ccf_2017', manifest='manifest.json')
    tree = rspc.get_structure_tree(structure_graph_id=1)
    name_map = tree.get_name_map()
    ancestor_map = tree.get_ancestor_id_map()
    area_count = {}
    n_not_found = 0
    area_unknown = {}
    for l in labels:
        try:
            ids = ancestor_map[int(l)]
        except KeyError:
            n_not_found += 1
            if 'unknown' not in area_count:
                area_count['unknown'] = 1
            else:
                area_count['unknown'] += 1
            if int(l) not in area_unknown:
                area_unknown[int(l)] = 1
            else:
                area_unknown[int(l)] += 1
            continue

        if len(ids) <= 2:
            id = ids[0]
        elif len(ids) <= n:
            id = ids[-2]
        else:
            id = ids[n if n < len(ids) - 1 else n - 1]

        # Get the name and store it
        name = name_map[id]
        if name not in area_count:
            area_count[name] = 1
        else:
            area_count[name] += 1

    # Display summary
    if n == 0:
        if n_not_found > 0:
            print('\nUnknown ontology ID found for {} objects ({:0.2f}%).'.format(n_not_found,
                                                                                  100*n_not_found/len(labels)))
            print('Unknown ontology IDs and occurrences:\n')
            print(area_unknown)
        else:
            print('\nAll objects were assigned to an atlas ontology category.\n')

    return area_count


def generate_csv(args, labels):
    """
    Generate new CSV with mapped object ID.

    Parameters
    ----------
    path: (str) path to the CSV file
    correct_labels: (array) mapped object ID

    Returns
    -------
    None
    """

    data = pd.read_csv(args.data_csv)
    data['Allen area ID'] = labels
    data.to_csv(os.path.join(args.output_path, 'mapped.csv'))


def main():
    # Parse argument from terminal call
    args = parse_arguments()
    # Create output directory if it does not exist
    Path(args.output_path).mkdir(parents=True, exist_ok=True)

    # Compute labels
    labels = get_labels(args)

    # Write label in original CSV
    generate_csv(args, labels)

    # Group by Allen ontology category
    for n in range(args.number_of_parents + 1):
        area_count = get_mapping(labels, n)
        area_df = pd.DataFrame.from_dict(area_count, orient='index')
        area_df.rename(columns={0: 'Number of detected objects'}, inplace=True)
        area_df.to_csv(os.path.join(args.output_path, 'ontology_parent_{}.csv').format(n))


if __name__ == '__main__':
    main()
