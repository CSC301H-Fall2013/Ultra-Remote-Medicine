package com.example.myapp;

import org.json.JSONArray;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TableRow;
import android.widget.TextView;

public class SearchResultActivity extends ActivityAPI {
	Context mContext;
	
	private int currentGroup = 0;
	
	private TextView sCaseIdA2;
	private TextView sCaseDateA3;
	private TextView sCaseSpecialtyA4;
	private TextView sCaseReviewerA5;
	private TextView sCasePriorityA6;

	private TextView sCaseIdB2;
	private TextView sCaseDateB3;
	private TextView sCaseSpecialtyB4;
	private TextView sCaseReviewerB5;
	private TextView sCasePriorityB6;

	private TextView sCaseIdC2;
	private TextView sCaseDateC3;
	private TextView sCaseSpecialtyC4;
	private TextView sCaseReviewerC5;
	private TextView sCasePriorityC6;

	private TextView sCaseIdD2;
	private TextView sCaseDateD3;
	private TextView sCaseSpecialtyD4;
	private TextView sCaseReviewerD5;
	private TextView sCasePriorityD6;
	
	private TextView sCaseIdE2;
	private TextView sCaseDateE3;
	private TextView sCaseSpecialtyE4;
	private TextView sCaseReviewerE5;
	private TextView sCasePriorityE6;
	
	private TextView sCaseIdF2;
	private TextView sCaseDateF3;
	private TextView sCaseSpecialtyF4;
	private TextView sCaseReviewerF5;
	private TextView sCasePriorityF6;
	
	private TextView sCaseIdG2;
	private TextView sCaseDateG3;
	private TextView sCaseSpecialtyG4;
	private TextView sCaseReviewerG5;
	private TextView sCasePriorityG6;

	private Button preButton;
	private Button nextButton;

	private TableRow stableRowA1Btn;
	private TableRow stableRowB1Btn;
	private TableRow stableRowC1Btn;
	private TableRow stableRowD1Btn;
	private TableRow stableRowE1Btn;
	private TableRow stableRowF1Btn;
	private TableRow stableRowG1Btn;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.search_result);
        mContext = this;
		preButton = (Button) findViewById(R.id.searchpage_pre_btn);
		nextButton = (Button) findViewById(R.id.searchpage_next_btn);
		
		sCaseIdA2 = (TextView) findViewById(R.id.searchpage_case_num_A2);
		sCaseDateA3 = (TextView) findViewById(R.id.searchpage_case_date_A3);
		sCaseSpecialtyA4 = (TextView) findViewById(R.id.searchpage_case_specialty_A4);
		sCaseReviewerA5 = (TextView) findViewById(R.id.searchpage_case_reviewer_A5);
		sCasePriorityA6 = (TextView) findViewById(R.id.searchpage_case_priority_A6);

		sCaseIdB2 = (TextView) findViewById(R.id.searchpage_case_num_B2);
		sCaseDateB3 = (TextView) findViewById(R.id.searchpage_case_date_B3);
		sCaseSpecialtyB4 = (TextView) findViewById(R.id.searchpage_case_specialty_B4);
		sCaseReviewerB5 = (TextView) findViewById(R.id.searchpage_case_reviewer_B5);
		sCasePriorityB6 = (TextView) findViewById(R.id.searchpage_case_priority_B6);

		sCaseIdC2 = (TextView) findViewById(R.id.searchpage_case_num_C2);
		sCaseDateC3 = (TextView) findViewById(R.id.searchpage_case_date_C3);
		sCaseSpecialtyC4 = (TextView) findViewById(R.id.searchpage_case_specialty_C4);
		sCaseReviewerC5 = (TextView) findViewById(R.id.searchpage_case_reviewer_C5);
		sCasePriorityC6 = (TextView) findViewById(R.id.searchpage_case_priority_C6);

		sCaseIdD2 = (TextView) findViewById(R.id.searchpage_case_num_D2);
		sCaseDateD3 = (TextView) findViewById(R.id.searchpage_case_date_D3);
		sCaseSpecialtyD4 = (TextView) findViewById(R.id.searchpage_case_specialty_D4);
		sCaseReviewerD5 = (TextView) findViewById(R.id.searchpage_case_reviewer_D5);
		sCasePriorityD6 = (TextView) findViewById(R.id.searchpage_case_priority_D6);

		sCaseIdE2 = (TextView) findViewById(R.id.searchpage_case_num_E2);
		sCaseDateE3 = (TextView) findViewById(R.id.searchpage_case_date_E3);
		sCaseSpecialtyE4 = (TextView) findViewById(R.id.searchpage_case_specialty_E4);
		sCaseReviewerE5 = (TextView) findViewById(R.id.searchpage_case_reviewer_E5);
		sCasePriorityE6 = (TextView) findViewById(R.id.searchpage_case_priority_E6);

		sCaseIdF2 = (TextView) findViewById(R.id.searchpage_case_num_F2);
		sCaseDateF3 = (TextView) findViewById(R.id.searchpage_case_date_F3);
		sCaseSpecialtyF4 = (TextView) findViewById(R.id.searchpage_case_specialty_F4);
		sCaseReviewerF5 = (TextView) findViewById(R.id.searchpage_case_reviewer_F5);
		sCasePriorityF6 = (TextView) findViewById(R.id.searchpage_case_priority_F6);

		sCaseIdG2 = (TextView) findViewById(R.id.searchpage_case_num_G2);
		sCaseDateG3 = (TextView) findViewById(R.id.searchpage_case_date_G3);
		sCaseSpecialtyG4 = (TextView) findViewById(R.id.searchpage_case_specialty_G4);
		sCaseReviewerG5 = (TextView) findViewById(R.id.searchpage_case_reviewer_G5);
		sCasePriorityG6 = (TextView) findViewById(R.id.searchpage_case_priority_G6);
		
		stableRowA1Btn = (TableRow) findViewById(R.id.searchpage_tableRowA1);
		stableRowB1Btn = (TableRow) findViewById(R.id.searchpage_tableRowB1);
		stableRowC1Btn = (TableRow) findViewById(R.id.searchpage_tableRowC1);
		stableRowD1Btn = (TableRow) findViewById(R.id.searchpage_tableRowD1);
		stableRowE1Btn = (TableRow) findViewById(R.id.searchpage_tableRowE1);
		stableRowF1Btn = (TableRow) findViewById(R.id.searchpage_tableRowF1);
		stableRowG1Btn = (TableRow) findViewById(R.id.searchpage_tableRowG1);
		
		loadSearchResult();
		
		// Button Click event for "pre" button
		preButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				// navigate to add new case page
				currentGroup--;
				loadSearchResult();
			}
		});

		// Button Click event for "next" button
		nextButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				// navigate to add new case page
				currentGroup++;
				loadSearchResult();
			}
		});

		// Button Click event for "RowA" button
		stableRowA1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurPatientId = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;
				JSONArray list = jsonCurSearchList.optJSONArray("result");
				jsonCurPatient = list.optJSONObject(currentGroup * 7);
				Intent i = new Intent(mContext, PatientPageActivity.class);
				startActivity(i);
			}
		});

		// Button Click event for "RowB" button
		stableRowB1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurPatientId = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;
				JSONArray list = jsonCurSearchList.optJSONArray("result");
				jsonCurPatient = list.optJSONObject(currentGroup * 7 + 1);
				Intent i = new Intent(mContext, PatientPageActivity.class);
				startActivity(i);
			}
		});

		// Button Click event for "RowC" button
		stableRowC1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurPatientId = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;
				JSONArray list = jsonCurSearchList.optJSONArray("result");
				jsonCurPatient = list.optJSONObject(currentGroup * 7 + 2);
				Intent i = new Intent(mContext, PatientPageActivity.class);
				startActivity(i);
			}
		});

		// Button Click event for "RowD" button
		stableRowD1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurPatientId = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;
				JSONArray list = jsonCurSearchList.optJSONArray("result");
				jsonCurPatient = list.optJSONObject(currentGroup * 7 + 3);
				Intent i = new Intent(mContext, PatientPageActivity.class);
				startActivity(i);
			}
		});
		
		// Button Click event for "RowE" button
		stableRowE1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurPatientId = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;
				JSONArray list = jsonCurSearchList.optJSONArray("result");
				jsonCurPatient = list.optJSONObject(currentGroup * 7 + 4);
				Intent i = new Intent(mContext, PatientPageActivity.class);
				startActivity(i);
			}
		});
		
		// Button Click event for "RowF" button
		stableRowF1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurPatientId = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;
				JSONArray list = jsonCurSearchList.optJSONArray("result");
				jsonCurPatient = list.optJSONObject(currentGroup * 7 + 5);
				Intent i = new Intent(mContext, PatientPageActivity.class);
				startActivity(i);
			}
		});
		
		// Button Click event for "RowG" button
		stableRowG1Btn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				jsonCurPatientId = null;
				jsonCurCaseList = null;
				jsonCurCaseId = null;
				jsonCurCase = null;
				JSONArray list = jsonCurSearchList.optJSONArray("result");
				jsonCurPatient = list.optJSONObject(currentGroup * 7 + 6);
				Intent i = new Intent(mContext, PatientPageActivity.class);
				startActivity(i);
			}
		});
    }
    
    private void loadSearchResult(){
		sCaseIdA2.setText("");
		sCaseDateA3.setText("");
		sCaseSpecialtyA4.setText("");
		sCaseReviewerA5.setText("");
		sCasePriorityA6.setText("");

		sCaseIdB2.setText("");
		sCaseDateB3.setText("");
		sCaseSpecialtyB4.setText("");
		sCaseReviewerB5.setText("");
		sCasePriorityB6.setText("");

		sCaseIdC2.setText("");
		sCaseDateC3.setText("");
		sCaseSpecialtyC4.setText("");
		sCaseReviewerC5.setText("");
		sCasePriorityC6.setText("");

		sCaseIdD2.setText("");
		sCaseDateD3.setText("");
		sCaseSpecialtyD4.setText("");
		sCaseReviewerD5.setText("");
		sCasePriorityD6.setText("");
		
		sCaseIdE2.setText("");
		sCaseDateE3.setText("");
		sCaseSpecialtyE4.setText("");
		sCaseReviewerE5.setText("");
		sCasePriorityE6.setText("");
		
		sCaseIdF2.setText("");
		sCaseDateF3.setText("");
		sCaseSpecialtyF4.setText("");
		sCaseReviewerF5.setText("");
		sCasePriorityF6.setText("");
		
		sCaseIdG2.setText("");
		sCaseDateG3.setText("");
		sCaseSpecialtyG4.setText("");
		sCaseReviewerG5.setText("");
		sCasePriorityG6.setText("");
		
		stableRowA1Btn.setEnabled(false);
		stableRowB1Btn.setEnabled(false);
		stableRowC1Btn.setEnabled(false);
		stableRowD1Btn.setEnabled(false);
		stableRowE1Btn.setEnabled(false);
		stableRowF1Btn.setEnabled(false);
		stableRowG1Btn.setEnabled(false);
		preButton.setEnabled(false);
		nextButton.setEnabled(false);
		

		if (jsonCurSearchList != null) {
			JSONArray list = jsonCurSearchList.optJSONArray("result");
			if (list.length() > 0) {
				int maxGroup = list.length() / 7;
				if (list.length() % 7 == 0){
					maxGroup--;
				}

				if (currentGroup <= 0) {
					// disable pre btn
					preButton.setEnabled(false);
				} else {
					// enable pre btn
					preButton.setEnabled(true);
				}
				if (currentGroup >= maxGroup) {
					// disable next btn
					nextButton.setEnabled(false);
				} else {
					// enable next btn
					nextButton.setEnabled(true);
				}

				// display case on first block
				sCaseIdA2.setText("Patient ID: "
						+ list.optJSONObject(currentGroup * 7).optString(
								"patient_id"));
				sCaseDateA3.setText("DOB: "
						+ list.optJSONObject(currentGroup * 7).optString(
								"date_of_birth"));
				sCaseSpecialtyA4.setText("Sex: "
						+ list.optJSONObject(currentGroup * 7).optString(
								"gender"));
				sCaseReviewerA5.setText("Name: "
						+ list.optJSONObject(currentGroup * 7).optString(
								"lastName"));
				sCasePriorityA6.setText("Addr: "
						+ list.optJSONObject(currentGroup * 7).optString(
								"address"));

				stableRowA1Btn.setEnabled(true);

				// display case on second block
				if (currentGroup != maxGroup || list.length() % 7 == 0
						|| list.length() % 7 > 1) {
					sCaseIdB2.setText("Patient ID: "
							+ list.optJSONObject(currentGroup * 7 + 1)
									.optString("patient_id"));
					sCaseDateB3.setText("DOB: "
							+ list.optJSONObject(currentGroup * 7 + 1)
									.optString("date_of_birth"));
					sCaseSpecialtyB4.setText("Sex: "
							+ list.optJSONObject(currentGroup * 7 + 1)
									.optString("gender"));
					sCaseReviewerB5.setText("Name: "
							+ list.optJSONObject(currentGroup * 7 + 1).optString(
									"lastName"));
					sCasePriorityB6.setText("Addr: "
							+ list.optJSONObject(currentGroup * 7 + 1)
									.optString("address"));

					stableRowB1Btn.setEnabled(true);
				}

				// display case on third block
				if (currentGroup != maxGroup || list.length() % 7 == 0
						|| list.length() % 7 > 2) {
					sCaseIdC2.setText("Patient ID: "
							+ list.optJSONObject(currentGroup * 7 + 2)
									.optString("patient_id"));
					sCaseDateC3.setText("DOB: "
							+ list.optJSONObject(currentGroup * 7 + 2)
									.optString("date_of_birth"));
					sCaseSpecialtyC4.setText("Sex: "
							+ list.optJSONObject(currentGroup * 7 + 2)
									.optString("gender"));
					sCaseReviewerC5.setText("Name: "
							+ list.optJSONObject(currentGroup * 7 + 2).optString(
									"lastName"));
					sCasePriorityC6.setText("Addr: "
							+ list.optJSONObject(currentGroup * 7 + 2)
									.optString("address"));
					stableRowC1Btn.setEnabled(true);
				}

				// display case on fourth block
				if (currentGroup != maxGroup || list.length() % 7 == 0
						|| list.length() % 7 > 3) {
					sCaseIdD2.setText("Patient ID: "
							+ list.optJSONObject(currentGroup * 7 + 3)
									.optString("patient_id"));
					sCaseDateD3.setText("DOB: "
							+ list.optJSONObject(currentGroup * 7 + 3)
									.optString("date_of_birth"));
					sCaseSpecialtyD4.setText("Sex: "
							+ list.optJSONObject(currentGroup * 7 + 3)
									.optString("gender"));
					sCaseReviewerD5.setText("Name: "
							+ list.optJSONObject(currentGroup * 7 + 3).optString(
									"lastName"));
					sCasePriorityD6.setText("Addr: "
							+ list.optJSONObject(currentGroup * 7 + 3)
									.optString("address"));
					stableRowD1Btn.setEnabled(true);
				}
				
				// display case on fourth block
				if (currentGroup != maxGroup || list.length() % 7 == 0
						|| list.length() % 7 > 4) {
					sCaseIdE2.setText("Patient ID: "
							+ list.optJSONObject(currentGroup * 7 + 4)
									.optString("patient_id"));
					sCaseDateE3.setText("DOB: "
							+ list.optJSONObject(currentGroup * 7 + 4)
									.optString("date_of_birth"));
					sCaseSpecialtyE4.setText("Sex: "
							+ list.optJSONObject(currentGroup * 7 + 4)
									.optString("gender"));
					sCaseReviewerE5.setText("Name: "
							+ list.optJSONObject(currentGroup * 7 + 4).optString(
									"lastName"));
					sCasePriorityE6.setText("Addr: "
							+ list.optJSONObject(currentGroup * 7 + 4)
									.optString("address"));
					stableRowE1Btn.setEnabled(true);
				}
				
				// display case on fourth block
				if (currentGroup != maxGroup || list.length() % 7 == 0
						|| list.length() % 7 > 5) {
					sCaseIdF2.setText("Patient ID: "
							+ list.optJSONObject(currentGroup * 7 + 5)
									.optString("patient_id"));
					sCaseDateF3.setText("DOB: "
							+ list.optJSONObject(currentGroup * 7 + 5)
									.optString("date_of_birth"));
					sCaseSpecialtyF4.setText("Sex: "
							+ list.optJSONObject(currentGroup * 7 + 5)
									.optString("gender"));
					sCaseReviewerF5.setText("Name: "
							+ list.optJSONObject(currentGroup * 7 + 5).optString(
									"lastName"));
					sCasePriorityF6.setText("Addr: "
							+ list.optJSONObject(currentGroup * 7 + 5)
									.optString("address"));
					stableRowF1Btn.setEnabled(true);
				}
				
				// display case on fourth block
				if (currentGroup != maxGroup || list.length() % 7 == 0) {
					sCaseIdG2.setText("Patient ID: "
							+ list.optJSONObject(currentGroup * 7 + 6)
									.optString("patient_id"));
					sCaseDateG3.setText("DOB: "
							+ list.optJSONObject(currentGroup * 7 + 6)
									.optString("date_of_birth"));
					sCaseSpecialtyG4.setText("Sex: "
							+ list.optJSONObject(currentGroup * 7 + 6)
									.optString("gender"));
					sCaseReviewerG5.setText("Name: "
							+ list.optJSONObject(currentGroup * 7 + 6).optString(
									"lastName"));
					sCasePriorityG6.setText("Addr: "
							+ list.optJSONObject(currentGroup * 7 + 6)
									.optString("address"));
					stableRowG1Btn.setEnabled(true);
				}

			}
		}
		
    }
}