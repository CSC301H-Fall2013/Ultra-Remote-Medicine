package org.nepalus;

import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;

import android.graphics.Bitmap;

public interface NepalUltrasoundAPI {	
	String getVersion();
	
	boolean setURL(String url);
	String getURL();
	
	HttpResponse send(String patientFirstName, 
			String patientLastName, String patientSex, String patientDOB,
			String patientHealthID, String patientGPSCoordinates, String patientAddress,
			String patientPhoneNumber, String patientEmail, Bitmap image)
		throws ClientProtocolException, IOException;
	
	HttpResponse sendcase(String patientID, 
			String patientPriority, String patientComments, Bitmap image)
		throws ClientProtocolException, IOException;
}
