package gov.lanl.gmd.output;


import gov.lanl.gmd.queries.Queries;
import gov.lanl.gmd.queries.TimeFormatter;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;

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
			// TODO Unsupported.			
			break;
		case HDF5:
			// TODO Unsupported.
			break;
		}
	}
	
	
	protected void writeMeasurements(ResultSet r){
		try {
			if(r.next()){
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
					// TODO Unsupported.
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
	
	protected void close(){
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
			// TODO Unsupported.
			break;
		case HDF5:
			// TODO Unsupported.
			break;
		}
		
	}


}
