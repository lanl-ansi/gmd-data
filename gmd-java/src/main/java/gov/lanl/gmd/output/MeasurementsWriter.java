package gov.lanl.gmd.output;


import gov.lanl.gmd.queries.TimeFormatter;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.codehaus.jackson.JsonEncoding;
import org.codehaus.jackson.JsonFactory;
import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.JsonGenerator;

public class MeasurementsWriter {
	
	public enum OutputType {CSV,JSON,HDF5};
	
	private OutputType outputType;
	private File file = null;
	private Object writer = null;
//	private String[] columnNames;

	protected MeasurementsWriter(String path, String prefix, OutputType outputType) {
		this.outputType = outputType;
		String filepath;
		switch(outputType){
		case CSV:
			filepath = path+"/"+prefix+".csv";
			file = new File(filepath);
			try {
				CSVPrinter printer = new CSVPrinter(new FileWriter(file),CSVFormat.DEFAULT);
				writer = printer;
			} catch (IOException e) {
				e.printStackTrace();
			}
			break;
		case JSON:
			filepath = path+"/"+prefix+".json";
			file = new File(filepath);
			JsonFactory jfactory = new JsonFactory();
			try {
				JsonGenerator jGenerator = jfactory.createJsonGenerator(new File(
						filepath), JsonEncoding.UTF8);
				jGenerator.writeStartArray();
				writer = jGenerator;
			} catch (IOException e) {
				e.printStackTrace();
			}
			break;
		case HDF5:
			// TODO Unsupported.
			break;
		}
	}
	
	
	public void writeMeasurements(ResultSet r) throws Exception {
		try {
			ResultSetMetaData metadata = r.getMetaData();
			int ncolumns = metadata.getColumnCount();
			String[] columnNames = new String[ncolumns];
			for(int i=0;i<ncolumns;i++){
				columnNames[i] = metadata.getColumnName(i+1);
			}
			boolean firstrecord = true;
			while(r.next()){
				Object[] record = new Object[ncolumns];
				// The timestamp is always the first.
				record[0] = TimeFormatter.formatTimestamp((Timestamp) r.getObject(1));
				for(int i=1;i<ncolumns;i++){
					record[i] = r.getObject(i+1);
				}

				switch(outputType){
				case CSV:
					CSVPrinter printer = (CSVPrinter) writer;
					if(firstrecord){
						printer.printRecord((Object[]) columnNames);
						firstrecord = false;
					}
					printer.printRecord(record);
					break;
				case JSON:
					JsonGenerator jGenerator = (JsonGenerator) writer;
					jGenerator.writeStartObject();
					// The timestamp is always first.
					jGenerator.writeStringField("timestamp", (String) record[0]);

					for(int i=1;i<ncolumns;i++){
						String typeName = metadata.getColumnTypeName(i+1);
						if(typeName.equals("varchar")){
							jGenerator.writeStringField(columnNames[i], (String) record[i]);
						} else if(typeName.equals("float8")){
							jGenerator.writeNumberField(columnNames[i], (double) record[i]);
						}
					}
					jGenerator.writeEndObject();
					break;
				case HDF5:
					// TODO Unsupported.
					break;
				}				
			}
		} catch (SQLException e) {
			throw e;
		} catch (IOException e1) {
			throw e1;
		}
	}
	
	public void close(){
		switch(outputType){
		case CSV:
			CSVPrinter printer = (CSVPrinter) writer;
			try {
				printer.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
			break;
		case JSON:
			JsonGenerator jGenerator = (JsonGenerator) writer;
			try {
				jGenerator.writeEndArray();
				jGenerator.close();
			} catch (JsonGenerationException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}			
			break;
		case HDF5:
			// TODO Unsupported.
			break;
		}
		
	}


}
