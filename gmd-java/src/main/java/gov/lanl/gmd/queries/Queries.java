package gov.lanl.gmd.queries;

import java.awt.geom.Point2D;
import java.awt.geom.Point2D.Double;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * A class containing useful static queries on the magneto database.
 */
public class Queries {

	enum CoordinateType {GEOGRAPHIC,MAGNETIC}
	enum MeasurementOption {
		MLON("mlon"),
		MLAT("mlat"),
		N("n"),
		E("e"),
		Z("z");
		private String value;	
		MeasurementOption(String value){
			this.value = value;
		}
		public String toString(){
			return value;
		}
	}

	/**
	 * A station record object.
	 */
	public static class Station{
		private String iaga;
		private double glon;
		private double glat;
		private double mlon;
		private double mlat;
		private String station_name;

		public Station(String iaga, double glon, double glat, double mlon,
				double mlat, String station_name) {
			this.iaga = iaga;
			this.glon = glon;
			this.glat = glat;
			this.mlon = mlon;
			this.mlat = mlat;
			this.station_name = station_name;
		}
		public String getIaga() {
			return iaga;
		}
		public double getGlon() {
			return glon;
		}
		public double getGlat() {
			return glat;
		}
		public double getMlon() {
			return mlon;
		}
		public double getMlat() {
			return mlat;
		}
		public String getStation_name() {
			return station_name;
		}
	}

	/**
	 * A measurement record object.
	 */
	public static class Measurement{
		private Timestamp date_utc;
		private String iaga;
		private double mlt;
		private double mlat;
		private double n;
		private double e;
		private double z;

		public Measurement(Timestamp date_utc, String iaga, double mlt,
				double mlat, double n, double e, double z) {
			this.date_utc = date_utc;
			this.iaga = iaga;
			this.mlt = mlt;
			this.mlat = mlat;
			this.n = n;
			this.e = e;
			this.z = z;
		}
		public Timestamp getDate_utc() {
			return date_utc;
		}
		public String getIaga() {
			return iaga;
		}
		public double getMlt() {
			return mlt;
		}
		public double getMlat() {
			return mlat;
		}
		public double getN() {
			return n;
		}
		public double getE() {
			return e;
		}
		public double getZ() {
			return z;
		}			
	}

	public static class MeasurementFilter{
		private MeasurementOption[] measurementOptions = null;		
		private String[] stationIDs = null;
		private Timestamp[] timeRange = null;
		private Point2D[] coordRange = null;
		private CoordinateType coordinateType = CoordinateType.GEOGRAPHIC;
		
		public MeasurementFilter() {}
		
		public MeasurementOption[] getMeasurementOptions() {
			return measurementOptions;
		}

		public void setMeasurementOptions(MeasurementOption[] measurementOptions) {
			this.measurementOptions = measurementOptions;
		}

		public String[] getStationIDs() {
			return stationIDs;
		}
		public void setStationIDs(String[] stationIDs) {
			this.stationIDs = stationIDs;
		}
		public Timestamp[] getTimeRange() {
			return timeRange;
		}
		public void setTimeRange(Timestamp initialTime, Timestamp finalTime) {
			this.timeRange = new Timestamp[2];
			this.timeRange[0] = initialTime;
			this.timeRange[1] = finalTime;
		}
		public Point2D[] getCoordRange() {
			return coordRange;
		}
		public void setCoordRange(double minlon, double minlat, double maxlon, double maxlat) {
			this.coordRange = new Point2D[2];
			this.coordRange[0] = new Point2D.Double(minlon,minlat);
			this.coordRange[1] = new Point2D.Double(maxlon,maxlat);
		}
		public CoordinateType getCoordinateType() {
			return coordinateType;
		}
		public void setCoordinateType(CoordinateType coordinateType) {
			this.coordinateType = coordinateType;
		}
	}

	/**
	 * Schema descriptions.
	 */
	private static final String[] tableNames = {"stations","measurements"};
	private static final String[] stationFieldNames = {"iaga","glon","glat","mlon","mlat","station_name"};
	private static final Class<?>[] stationFieldTypes = {String.class, Double.class, Double.class,
		Double.class, Double.class, String.class};
	private static final Map<String,Class<?>> stationFields = new HashMap<>();
	static{
		for(int i=0;i<stationFieldNames.length;i++){
			stationFields.put(stationFieldNames[i], stationFieldTypes[i]);
		}
	}
	private static final String[] measurementFieldNames = {"date_utc","iaga","mlt","mlat","n","e","z","collection"};
	private static final Class<?>[] measurementFieldTypes = {Timestamp.class, String.class, Double.class,
		Double.class, Double.class, Double.class, Double.class, String.class};
	private static final Map<String,Class<?>> measurementFields = new HashMap<>();
	static{
		for(int i=0;i<measurementFieldNames.length;i++){
			measurementFields.put(measurementFieldNames[i], measurementFieldTypes[i]);
		}		
	}

	/**
	 * Returns a list of table names.
	 * @return
	 */
	protected static String[] getTableNames(){
		return tableNames;
	}

	/**
	 * Returns a list of station field names.
	 * @return
	 */
	public static String[] getStationFieldNames(){
		return stationFieldNames;
	}
	
	/**
	 * Returns a dictionary of station field names and types.
	 * @return
	 */
	public static Map<String,Class<?>> getStationFields(){
		return stationFields;
	}

	/**
	 * Returns a list of Station field types.
	 * @return
	 */
	protected static Class<?>[] getStationFieldTypes(){
		return stationFieldTypes;
	}

	/**
	 * Returns a list of measurement field names.
	 * @return
	 */
	public static String[] getMeasurementFieldNames(){
		return measurementFieldNames;
	}
	
	/**
	 * Returns a dictionary of measurement field names and types.
	 * @return
	 */
	public static Map<String,Class<?>> getMeasurementFields(){
		return measurementFields;
	}

	/**
	 * Returns a list of measurement field types.
	 * @return
	 */
	protected static Class<?>[] getMeasurementFieldTypes(){
		return measurementFieldTypes;
	}
	
	

	private static ResultSet queryMagneto(Connection conn, String queryString){
		ResultSet r = null;
		try {
			Statement statement = conn.createStatement();
			r = statement.executeQuery(queryString);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return r;
	}

	/**
	 * Returns a map of all station objects.
	 * @param conn
	 * @return
	 */
	public static Map<String,Station> getStations(Connection conn){
		String queryString = "select * from magneto.stations order by iaga";
		ResultSet r = queryMagneto(conn, queryString);
		return getStations(r);
	}


	public static Map<String,Station> getStationsByGeoCoords(Connection conn,
			double glonmin, double glatmin, double glonmax, double glatmax){
		String queryString = "select * from magneto.stations where"+
				" glon >= "+glonmin +" and glon <= "+glonmax+
				" and glat >= "+glatmin+" and glat <= "+glatmax+ " order by iaga";
		ResultSet r = queryMagneto(conn, queryString);
		return getStations(r);
	}

	public static Map<String,Station> getStationsByMagCoords(Connection conn,
			double mlonmin, double mlatmin, double mlonmax, double mlatmax){
		String queryString = "select * from magneto.stations where"+
				" mlon >= "+mlonmin+" and mlon <= "+mlonmax+
				" mlat >= "+mlatmin+" and mlat <= "+mlatmax+ " order by iaga";
		ResultSet r = queryMagneto(conn, queryString);
		return getStations(r);
	}

	private static Map<String,Station> getStations(ResultSet r){
		Map<String,Station> stations = null;
		try {
			if(r.next()){
				stations = new HashMap<>();
				while(r.next()){
					String iaga = r.getString("iaga");
					double glon = r.getDouble("glon");
					double glat = r.getDouble("glat");
					double mlon = r.getDouble("mlon");
					double mlat = r.getDouble("mlat");
					String station_name = r.getString("station_name");
					stations.put(iaga, new Station(iaga,glon,glat,mlon,mlat,station_name));
				}
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return stations;
	}

	public static ResultSet filterMeasurements(Connection conn, MeasurementFilter filter){
		ResultSet r = null;
		String[] stationIDs = filter.getStationIDs();
		Timestamp[] timeRange = filter.getTimeRange();
		Point2D[] coordRange = filter.getCoordRange();
		CoordinateType coordinateType = filter.getCoordinateType();
		if(timeRange!=null){ // Some type of time filter is required to perform the query.
			List<String> clauses = new ArrayList<>();
			Set<String> stationIDSet = null;
			// Station ID filter selects specific stations by ID.
			if(stationIDs!=null){
				if(stationIDSet==null){
					stationIDSet = new HashSet<>();
				}
				for(String stationID : stationIDs){
					stationIDSet.add(stationID);
				}
			}
			// Coordinate range filter selects stations by location.
			if(coordRange!=null){
				if(stationIDSet==null){
					stationIDSet = new HashSet<>();
				}
				Map<String,Station> stations = null;
				switch(coordinateType){
				case GEOGRAPHIC:
					stations = Queries.getStationsByGeoCoords(conn,coordRange[0].getX(),coordRange[0].getY(),
							coordRange[1].getX(),coordRange[1].getY());
					break;
				case MAGNETIC:
					stations = Queries.getStationsByMagCoords(conn,coordRange[0].getX(),coordRange[0].getY(),
							coordRange[1].getX(),coordRange[1].getY());
					break;
				}
				if(stations!=null){
					for(String stationID : stations.keySet()){
						stationIDSet.add(stationID);
					}
				}
			}
			// If the station set is not null, or empty, create a stations clause.
			if(stationIDSet!=null){
				if(stationIDSet.size()>0){
					String[] stationArray = stationIDSet.toArray(new String[0]);
					StringBuilder stationsClause = new StringBuilder("iaga = any(array['"+stationArray[0]);
					for(int i=1;i<stationArray.length;i++){
						stationsClause.append("','" + stationArray[i]);
					}
					stationsClause.append("'])");
					clauses.add(stationsClause.toString());
				}
			}
			if(timeRange!=null){
				StringBuilder timeRangeClause = new StringBuilder();
				timeRangeClause.append("date_utc >= '" + TimeFormatter.formatTimestamp(timeRange[0]));
				timeRangeClause.append("' and date_utc <= '" + TimeFormatter.formatTimestamp(timeRange[1])+"'");
				clauses.add(timeRangeClause.toString());
			}
			// Build the query string from the clauses.
			MeasurementOption[] measurementOptions = filter.getMeasurementOptions();
			StringBuilder columnSelection = new StringBuilder("date_utc,iaga");
			if(measurementOptions!=null)
			{
				columnSelection.append(","+measurementOptions[0]);
				for(int i=1;i<measurementOptions.length;i++){
					columnSelection.append(","+measurementOptions[i]);
				}
				columnSelection.append(",collection");
			} else{
				columnSelection.append("*");
			}
			StringBuilder queryString = new StringBuilder("select "+columnSelection.toString()
					+ " from magneto.measurements where ");
			queryString.append(clauses.get(0));
			if(clauses.size()>1){
				queryString.append(" and "+clauses.get(1));
			}
			queryString.append(" order by date_utc;");
			// System.out.println(queryString.toString());
			r = queryMagneto(conn,queryString.toString());
		}
		return r;
	}


}
