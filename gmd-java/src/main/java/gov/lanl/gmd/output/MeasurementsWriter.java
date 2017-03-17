package gov.lanl.gmd.output;


import gov.lanl.gmd.queries.Queries;
import gov.lanl.gmd.queries.TimeFormatter;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;

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
				Object[] headers = (Object[]) Queries.getMeasurementFieldNames();
				printer.printRecord(headers);
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
	
	
	public void writeMeasurements(ResultSet r){
		try {
			while(r.next()){
				Timestamp date_utc = r.getTimestamp("date_utc");
				String timestamp = TimeFormatter.formatTimestamp(date_utc);
				String iaga = r.getString("iaga");
				double mlt = r.getDouble("mlt");
				double mlat = r.getDouble("mlat");
				double n = r.getDouble("n");
				double e = r.getDouble("e");
				double z = r.getDouble("z");
				String collection = r.getString("collection");

				switch(outputType){
				case CSV:
					CSVPrinter printer = (CSVPrinter) writer;
					printer.printRecord(timestamp,iaga,mlt,mlat,n,e,z,collection);
					break;
				case JSON:
					JsonGenerator jGenerator = (JsonGenerator) writer;
					jGenerator.writeStartObject();
					jGenerator.writeStringField("timestamp", timestamp);
					jGenerator.writeStringField("iaga", iaga);				
					jGenerator.writeNumberField("mlt", mlt);
					jGenerator.writeNumberField("mlat", mlat);
					jGenerator.writeNumberField("n", n);
					jGenerator.writeNumberField("e", e);
					jGenerator.writeNumberField("z", z);
					jGenerator.writeStringField("collection", collection);				
					jGenerator.writeEndObject();
					break;
				case HDF5:
					// TODO Unsupported.
					break;
				}				
			}
		} catch (SQLException e) {
			e.printStackTrace();
		} catch (IOException e1) {
			e1.printStackTrace();
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
