package com.example.myapp;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;

public class ActivityAPI extends Activity {
	public static JSONObject jsonCurSessionId;
	public static JSONObject jsonCurPatientId;
	public static JSONObject jsonCurPatient;
	public static JSONObject jsonCurCaseList;
	public static JSONObject jsonCurCaseId;
	public static JSONObject jsonCurCase;
	public static final String SESSIONID = "SessionId";
	
	public static JSONObject communicate(String urlString, String jsonString) {
		try {
			byte[] data = jsonString.getBytes();
			
			//urlString = "http://ultra-remote-medicine.herokuapp.com/mobile/" + urlString;
			urlString = "http://10.0.2.2:8000/mobile/" + urlString;
			
			// build connection
			URL url = new URL(urlString);
			HttpURLConnection connection = (HttpURLConnection) url
					.openConnection();
			connection.setDoOutput(true);
			connection.setDoInput(true);
			connection.setFixedLengthStreamingMode(data.length);

			// write data to the server
			OutputStream outputStream = connection.getOutputStream();
			outputStream.write(data);

			// read feedback
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					connection.getInputStream()));
			String lines;
			StringBuffer sb = new StringBuffer("");
			while ((lines = reader.readLine()) != null) {
				lines = new String(lines.getBytes());
				sb.append(lines);
			}
			reader.close();
			// disconnect the server
			connection.disconnect();
			// pack the json and return it.
			String out = sb.toString();
			JSONObject jo;
			if (out != null){
				jo = new JSONObject(out);
			} else {
				jo = null;
			}
			return jo;
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (JSONException e) {
			e.printStackTrace();
		}
		return null;
	}
}
