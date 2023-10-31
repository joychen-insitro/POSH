import json
def build_workflow_json(barcode, cycle_acquisitions):
    header = {}
    header["plate_id_out_path"] = barcode 
    cell_extent_acquisition = {}
    cell_extent_acquisition["plate_barcode"] = barcode
    cell_extent_acquisition["measurement_id"] = cycle_acquisitions[1] 
    cell_extent_acquisition["dataframe"] = os.path.join("s3://insitro-microscopy-data/prod/pyxcell/", barcode, "canonical_image_qc", cycle_acquisitions[1], "canonical_plate_acquisition_filtered.pq")
    cell_extent_acquisition["source_microscope"] = "COMMON_CANONICAL"
    cell_extent_acquisition["image_storage_format"] = 1
    cell_extent_acquisition["image_orientation"] = "N"
    
    channel_mapping = {}
    channel_mapping["DAPI"] = "posh_nucleus"
    channel_mapping["G"] = "posh_g"
    channel_mapping["T"] = "posh_t"
    channel_mapping["A"] = "posh_a"
    channel_mapping["C"] = "posh_c"
    cell_extent_acquisition["channel_mapping"]= channel_mapping
      
    

    header["cell_extent_acquisition"] = cell_extent_acquisition
   
  
    header["readout_acquisitions"] = []
    sbs_acquisitions = {}

    for cycle, acq_id in cycle_acquisitions.items():
        thiscycle = {}
        thiscycle["plate_barcode"] = barcode
        thiscycle["measurement_id"] = acq_id
        thiscycle["dataframe"] = os.path.join("s3://insitro-microscopy-data/prod/pyxcell/", barcode, "canonical_image_qc" , acq_id, "canonical_plate_acquisition_filtered.pq")
        thiscycle["source_microscope"] = "COMMON_CANONICAL"
        thiscycle["image_storage_format"] = 1
        thiscycle["image_orientation"] = "N"
        thiscycle["channel_mapping"] = channel_mapping
        sbs_acquisitions[cycle] = thiscycle

    header["sbs_acquisitions"] = sbs_acquisitions

    
    segmenter = {} 
    segmenter["name"] = "CellposePublicNucleiSegmenter"
    seg_args = {}
    seg_args["inference_device"] =  "cpu"
    segmenter["args"] = seg_args
    header["primary_segmenter"] = segmenter
    header["secondary_segmenters"] = []
    header["feature_extractors"] =  []
    header["adjust_stage_coordinates"] = True
    cal_crop_ratios = {}
    for acq_id in cycle_acquisitions.values():
        cal_crop_ratios[acq_id] = 1
    header["calibration_crop_ratios"] = cal_crop_ratios
    header["base_out_path"] = "s3://insitro-microscopy-data/prod/pyxcell"
    header["tile_side_length_pixels"] = 224
    header["registration_image_crop_size_pixels"] =  10000
    header["rescaled_registration_image_size_pixels"] = 10000
    header["neighbor_determination_margin_of_error_pixels"] = 150
    header["guide_library_file"] = "s3://insitro-microscopy-data/prod/pyxcell/PA17000/workflow_specs/wgA549_pool2_1_library.pq"
   

    with open(f'{barcode}_iss_workflow.json', 'w') as fp:
      json.dump(header, fp, indent=1)
    return  