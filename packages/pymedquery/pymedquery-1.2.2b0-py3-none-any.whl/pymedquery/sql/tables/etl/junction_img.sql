/* This table is meant to be a connection table for other tables and contains
 the most important identifier for the fetching data on the images. Notice that there are
 only FKs for the UIDs. That is because an UID can be included in more than one project*/

CREATE TABLE IF NOT EXISTS junction_img_table (
	patient_uid TEXT NOT NULL,
	project_id TEXT NOT NULL,
	study_uid TEXT NOT NULL,
    FOREIGN KEY (study_uid) REFERENCES study_table (study_uid)
    FOREIGN KEY (patient_uid) REFERENCES patient_table (patient_uid)
);
