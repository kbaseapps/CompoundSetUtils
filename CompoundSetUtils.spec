/*
A KBase module: CompoundSetUtils
Contains tools for import & export of compound sets
*/

module CompoundSetUtils {
    typedef string obj_ref;

    typedef structure {
        string workspace_name;
        string staging_file_path;
        string compound_set_name;
    } compoundset_upload_params;

    typedef structure {
        string report_name;
        string report_ref;
        obj_ref compoundset_ref;
    } compoundset_upload_results;

    /*
        CompoundSetFromFile
        string staging_file_path
    */

    funcdef compound_set_from_file(compoundset_upload_params params)
        returns (compoundset_upload_results output) authentication required;

    typedef structure {
        string report_name;
        string report_ref;
    } compoundset_download_results;

    typedef structure {
        string workspace_name;
        string compound_set_name;
        string output_format;
    } compoundset_download_params;

    /*
        CompoundSetToFile
        string compound_set_name
        string output_format
    */

    funcdef compound_set_to_file(compoundset_download_params params)
        returns (compoundset_download_results output) authentication required;

    typedef structure {
        string workspace_name;
        string model_name;
        string compound_set_name;
    } compoundset_from_model_params;

    /*
        CompoundSetFromModel
        required:
        string workspace_name
        string model_name
        string compound_set_name
    */

    funcdef compound_set_from_model(compoundset_from_model_params params)
        returns (compoundset_upload_results output) authentication required;

    /*  input and output structure functions for standard downloaders */
    typedef structure {
        string input_ref;
    } ExportParams;

    typedef structure {
        string shock_id;
    } ExportOutput;

    funcdef export_compoundset_as_tsv(ExportParams params)
        returns (ExportOutput output) authentication required;

    funcdef export_compoundset_as_sdf(ExportParams params)
        returns (ExportOutput output) authentication required;
};