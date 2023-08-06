#!/usr/bin/env python3

"""Module containing the BioBBs DisGeNET class and the command line interface."""
import argparse
import shutil
import pandas as pd
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_disgenet.disgenet.common import *


# 1. Rename class as required
class CNV_disgenet(BiobbObject):
    """
    | biobb_disgenet for Disgenet
    | This class is for converting any Associations file from DisGeNET database into a txt/cvs format.
    | Wrapper for the DisGeNET database `https://www.disgenet.org` and the  DisGeNET REST API ´https://www.disgenet.org/api/´ for downloading available collections of genes and variants associated data to human diseases.

    Args:
        
        input_file_path(str): input path of the file download directly from DisGeneT REST API (that can be in format TSV, JSON or XML).
        output_file_path (str): Path to the output file, that can be in format TSV, JSON or XML. 
        
        properties (dict - Python dict containing the properties for the API interrogation, considering also the credentials of the user to the database):
            * **gene_id** (*str*) - Number identification for a gene or a list of genes separated by commas recognized by the database.
            * **disease** (*str*) - Disease id or a list of disease separated by commas.
            * **disease_type** (*str*) - Disease, phenotype, group.
            * **source** (*str*) - Source of the associations (CURATED, INFERRED, ANIMAL_MODELS, ALL, BEFREE, CGI, CLINGEN, CLINVAR, CTD_human, CTD_mouse, CTD_rat, GENOMICS_ENGLAND, GWASCAT, GWASDB, HPO, LHGDN, MGD, ORPHANET, PSYGENET, RGD, UNIPROT).
            * **disease_vocabulary** (*str*) - Disease vocabulary (icd9cm, icd10, mesh, omim, do, efo, nci, hpo, mondo, ordo).
            * **disease_class** * - MeSh disease classes.
            * **min_score** (*str*) -  Min value of the gene-disease score range.
            * **max_score** (*str*) -  Max value of the gene-disease score range.
            * **min_ei** (*str*) -  Min value of evidence index score range.
            * **max_ei** (*str*) -  Max value of evidence index score range.
            * **max_dsi** (*str*) - Max value of DSI range for the gene.
            * **min_dsi** (*str*)  - Min value of DSI range for the gene.
            * **max_pli** (*str*) -  Max value of pLI range for the gene.
            * **min_pli** (*str*) -  Min value of pLI range for the gene.
            * **format** (*str*) - Format output file.
            * **limit** (*str*) - Number of GDAs to retrieve.
            * **min_year** (*str*) - The year of the earliest publications.
            * **max_year** (*str*) - The year of the latest publicatons.
            * **offset** (*str*) - Starting offset of the page.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python:

            from biobb_disgenet.disgenet.gda_disgenet import gda_disgenet

            prop = { 
                'gene_id': 'gene_id',
                'disease_id': 'disease_id',
                'uniprot_id': 'uniprot_id',
                'source': 'source', 
                'min_score': 'min_score',
                'max_score': 'max_score',
                'min_ei': 'min_ei',
                'max_ei': 'max_ei',
                'type': 'disease_type',
                'disease_class': 'disease_class',
                'min_dsi': 'min_dsi',
                'max_dsi': 'max_dsi',
                'min_dpi': 'min_dpi',
                'max_dpi': 'max_dpi',
                'min_pli': 'min_pli',
                'max_pli':'max_pli', 
                'format': 'format',
                'limit': 'limit',
                'min_year':'min_year',
                'max_year':'max_year',
                'offset':'offset'
            }
            gda_disgenet(retrieve_by='gene',
                    output_file_path='output_gene_351',
                    properties=prop)
    Info:

        retrieve_by can be: 
            gene, uniprot, source, evidences

    """

    # 2. Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, input_file_path, output_file_path,
                properties = None, **kwargs) -> None:
        properties = properties or {}

        # 2.0 Call parent class constructor
        super().__init__(properties)

        # 2.1 Modify to match constructor parameters
        # Input/Output files
        self.io_dict = { 
                'in': {'input_file_path': input_file_path}, 
            'out': { 'output_file_path': output_file_path } 
        }

        # 3. Include all relevant properties here as 
        # self.property_name = properties.get('property_name', property_default_value)

        # Properties specific for BB
        bb_properties = {}
        
        self.format = properties.get('format', 'txt')

        #print (properties)
        #print (self.email, self.password)
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`GDA_disgenet <disgenet.GDA_disgenet.GDA_disgenet>` object."""
        
        # 4. Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()
        
        #self.check_data_params(self.out_log, self.err_log)

        #Check if the output path exists and mandatory params are there
        output_path = check_output_path(self.io_dict["out"]["output_file_path"], False, "output", self.format, self.out_log, self.__class__.__name__)

#      new_keys, request = extension_request(response, self.io_dict["in"]["retrieve_by"], self.properties)
#        auth_session(request, new_keys, self.email,self.password, output_path, self.out_log, self.global_log)

        new_file = output_path+ "_converted"

        if os.path.isfile(self.io_dict["in"]["input_file_path"]):
            print (self.io_dict["in"]["input_file_path"])
            convert_file(self.io_dict["in"]["input_file_path"], self.io_dict["out"]["output_file_path"], ".txt", self.out_log, self.global_log)

        #Authorized the session based on the session request
        #if output_path:
            #convert_file(self.io_dict["in"]["input_file_path"], self.io_dict["out"]["output_file_path"], self.format)
        #if self.io_dict["in"]["retrieve_by"]:
        #    response = gda_vda_session("gda", self.io_dict["in"]["retrieve_by"], self.properties, self.out_log, self.global_log)
        else:
            raise SystemExit("Fundamental argument is missing, check the input parameter.")
        
        #new_keys, request = extension_request(response, self.io_dict["in"]["retrieve_by"], self.properties)
        #auth_session(request, new_keys, self.email,self.password, output_path, self.out_log, self.global_log)       
        
        return 0

def cnv_disgenet(input_file_path: str, output_file_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`Template <template.template.Template>` class and
    execute the :meth:`launch() <template.template.Template.launch>` method."""

    return CNV_disgenet(
                    input_file_path=input_file_path,
                    output_file_path=output_file_path,
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='This class is a wrapper for an associations call of teh DisGeNET database REST API.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # 10. Include specific args of each building block following the examples. They should match step 2
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-input_file_path', required=True, help='')
    required_args.add_argument('-output_file_path', required=True, help='Description for the output file path. Accepted formats: json, csv or html.')
    #required_args.add_argument('-email',  required=True)
    #required_args.add_argument('-password',  required=True)
    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # 11. Adapt to match Class constructor (step 2)
    # Specific call of each building block
    cnv_disgenet(
             input_file_path=input_file_path,
             output_file_path=output_file_path,
             properties=properties)

if __name__ == '__main__':
    main()

# 12. Complete documentation string


