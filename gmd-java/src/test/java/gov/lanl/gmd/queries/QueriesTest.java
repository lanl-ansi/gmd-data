package gov.lanl.gmd.queries;

import java.awt.geom.Point2D;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import gov.lanl.gmd.dbconnect.DBConnector;
import gov.lanl.gmd.queries.Queries.CoordinateType;
import gov.lanl.gmd.queries.Queries.Station;
import gov.lanl.gmd.queries.Queries.MeasurementFilter;


import junit.framework.Assert;
import junit.framework.TestCase;

public class QueriesTest extends TestCase {
	
	private static String[] testStations = {
			"A02","A03","A04","A05","A06","A07",
			"A08","A09","A10","A11"};		
    private static String initialTimestamp = "2001-10-02 18:00:00";
    private static Timestamp initialTime = Timestamp.valueOf(initialTimestamp);
    private static String finalTimestamp = "2001-10-02 18:01:00";
	private static Timestamp finalTime = Timestamp.valueOf(finalTimestamp);
	private static double minlon=-166.03, minlat=59.59,
			maxlon=-141.90, maxlat=70.88; // Alaska

	
	public void testStationsQuery(){
//		String[] testStations = {
//				"A02","A03","A04","A05","A06","A07",
//				"A08","A09","A10","A11"};		
		DBConnector connector = new DBConnector();
		Connection conn = connector.getConnection();
		Map<String,Station> stations = Queries.getStations(conn);
		List<String> iaga = new ArrayList<String>(stations.keySet());
		Collections.sort(iaga);
		for(int i=0;i<10;i++){
			Assert.assertTrue(iaga.get(i).equals(testStations[i]));
		}
		connector.closeConnection();
	}
	
	public void testStationsByGeoQuery(){
//		double minlon=-166.03, minlat=59.59, maxlon=-141.90, maxlat=70.88; // Alaska
		String[] sortedTestStations = {"ARC", "BET", "CGO", "CMO", "DED", "FYU", "GAK",
				"HLM", "HOM", "JCO", "KAV", "KOT", "PKR", "T39", "T40", "T41", "TLK"};
		DBConnector connector = new DBConnector();
		Connection conn = connector.getConnection();
		Map<String,Station> stations = Queries.getStationsByGeoCoords(conn, minlon, minlat, maxlon, maxlat);
		List<String> iaga = new ArrayList<String>(stations.keySet());
		Collections.sort(iaga);
		for(int i=0;i<sortedTestStations.length;i++){
			Assert.assertTrue(iaga.get(i).equals(sortedTestStations[i]));
		}
		connector.closeConnection();
	}
	
	public void testMeasurementFilter(){
//		MeasurementFilter filter = new MeasurementFilter();
//		String[] testStations = {
//				"A02","A03","A04","A05","A06","A07",
//				"A08","A09","A10","A11"};		
//		filter.setStationIDs(testStations);
//		
//        String initialTimestamp = "2001-10-02 18:00:00";
//        Timestamp initialTime = Timestamp.valueOf(initialTimestamp);
//        String finalTimestamp = "2001-10-02 18:01:00";
//		Timestamp finalTime = Timestamp.valueOf(finalTimestamp);
//		filter.setTimeRange(initialTime, finalTime);
//		
//		double minlon=-166.03, minlat=59.59, maxlon=-141.90, maxlat=70.88;
//		filter.setCoordRange(minlon, minlat, maxlon, maxlat);
		MeasurementFilter filter = makeTestFilter();
		
		String[] stationIds = filter.getStationIDs();
		for(int i=0;i<testStations.length;i++){
			Assert.assertTrue(stationIds[i].equals(testStations[i]));
		}
		
		Timestamp[] timerange = filter.getTimeRange();
		Assert.assertTrue(timerange[0].equals(initialTime));
		Assert.assertTrue(timerange[1].equals(finalTime));
		
		Point2D[] coordrange = filter.getCoordRange();
		Assert.assertTrue(coordrange[0].getX()==minlon);
		Assert.assertTrue(coordrange[0].getY()==minlat);
		Assert.assertTrue(coordrange[1].getX()==maxlon);
		Assert.assertTrue(coordrange[1].getY()==maxlat);
		
		CoordinateType coordtype = filter.getCoordinateType();
		Assert.assertTrue(coordtype.equals(CoordinateType.GEOGRAPHIC));
		
		filter.setCoordinateType(CoordinateType.MAGNETIC);
		coordtype = filter.getCoordinateType();	
		Assert.assertTrue(coordtype.equals(CoordinateType.MAGNETIC));
	}
	
	public void testMeasurementQuery(){
		// Just test to see if a measurement query runs.
		DBConnector connector = new DBConnector();
		Connection conn = connector.getConnection();
		MeasurementFilter filter = makeTestFilter();
		ResultSet r = Queries.filterMeasurements(conn, filter);
		try {
			Assert.assertTrue(r.next());
		} catch (SQLException e) {
			Assert.assertFalse(false);
			e.printStackTrace();
		}
		
		
		
	}
	
	private MeasurementFilter makeTestFilter(){
		MeasurementFilter filter = new MeasurementFilter();
//		String[] testStations = {
//				"A02","A03","A04","A05","A06","A07",
//				"A08","A09","A10","A11"};		
		filter.setStationIDs(testStations);
		
//        String initialTimestamp = "2001-10-02 18:00:00";
//        Timestamp initialTime = Timestamp.valueOf(initialTimestamp);
//        String finalTimestamp = "2001-10-02 18:01:00";
//		Timestamp finalTime = Timestamp.valueOf(finalTimestamp);
		filter.setTimeRange(initialTime, finalTime);
		
//		double minlon=-166.03, minlat=59.59, maxlon=-141.90, maxlat=70.88;
		filter.setCoordRange(minlon, minlat, maxlon, maxlat);
		return filter;
	}

}
