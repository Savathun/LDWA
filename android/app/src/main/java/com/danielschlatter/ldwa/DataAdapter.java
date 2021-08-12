package com.danielschlatter.ldwa;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class DataAdapter {

    protected static final String TAG = "DataAdapter";

    private SQLiteDatabase mDb;
    private final DataBaseHelper mDbHelper;

    public DataAdapter(Context context) {
        mDbHelper = new DataBaseHelper(context);
    }

    public void createDatabase() throws SQLException {
        try {
            mDbHelper.createDataBase();

        } catch (IOException mIOException) {
            Log.e(TAG, mIOException.toString() + "  UnableToCreateDatabase");
            throw new Error("UnableToCreateDatabase");
        }
    }

    public void open() throws SQLException {
        try {
            mDbHelper.openDataBase();
            mDbHelper.close();
            mDb = mDbHelper.getReadableDatabase();
        } catch (SQLException mSQLException) {
            Log.e(TAG, "open >>"+ mSQLException.toString());
            throw mSQLException;
        }
    }

    public void close() {
        mDbHelper.close();
    }

    public Cursor selectAll() {
        try {
            return mDb.rawQuery("select * from weapons order by name", null);
        } catch (SQLException mSQLException) {
            Log.e(TAG, "selectall failed "+ mSQLException.toString());
            throw mSQLException;
        }
    }
    public String selectPerk(String name) {
        try {
            Cursor mCur = mDb.rawQuery("select displayProperties_icon from perks where displayProperties_name = ?" , new String[] {name});
            mCur.moveToNext();
            String path = mCur.getString(mCur.getColumnIndex("displayProperties_icon"));
            mCur.close();
            return path.substring(25, path.length()-4).replace('/', '_');
        } catch (SQLException mSQLException) {
            Log.e(TAG, "selectperk failed"+ mSQLException.toString() + name);
            throw mSQLException;
        }
    }
    public void insertRoll(String weapon, int p1, int p2, int p3, int p4){
        ContentValues cv = new ContentValues();
        cv.put("weapon", weapon); cv.put("p1", p1); cv.put("p2", p2); cv.put("p3", p3); cv.put("p4", p4);
        mDb.insert("saved_rolls", null, cv);
    }
    public void removeRoll(String weapon, int p1, int p2, int p3, int p4){
        mDb.delete("saved_rolls", "weapon = ? and p1 = ? and p2 = ? and p3 = ? and p4 = ?",
                new String []{weapon, String.valueOf(p1), String.valueOf(p2), String.valueOf(p3), String.valueOf(p4)});
    }

    public Cursor selectRolls(String weapon){
        return mDb.rawQuery("select * from saved_rolls where weapon = ?", new String[]{weapon});
    }
    private static class DataBaseHelper extends SQLiteOpenHelper {

        private static final String TAG = "DataBaseHelper"; // Tag just for the LogCat window
        private static final String DB_NAME ="weapons_database.sqlite"; // Database name
        private static final int DB_VERSION = 1; // Database version
        private final File DB_FILE;
        private SQLiteDatabase mDataBase;
        private final Context mContext;

        public DataBaseHelper(Context context) {
            super(context, DB_NAME, null, DB_VERSION);
            DB_FILE = context.getDatabasePath(DB_NAME);
            this.mContext = context;
        }

        public void createDataBase() throws IOException {
            // If the database does not exist, copy it from the assets.
            boolean mDataBaseExist = checkDataBase();
            if(!mDataBaseExist) {
                this.getReadableDatabase();

                this.close();

                // Copy the database from assests
                copyDataBase();
                Log.e(TAG, "createDatabase database created");
                openDataBase();
                try{
                    mDataBase.execSQL("create table saved_rolls(weapon text, p1 int, p2 int, p3 int, p4 int)");
                } catch (SQLException mSQLException) {
                    Log.e(TAG, "table select_rolls creation failed >>"+ mSQLException.toString());
                    throw mSQLException;
                }
            }
        }

        // Check that the database file exists in databases folder
        private boolean checkDataBase() {
            return DB_FILE.exists();
        }

        // Copy the database from assets
        private void copyDataBase() throws IOException {
            InputStream mInput = mContext.getAssets().open(DB_NAME);
            OutputStream mOutput = new FileOutputStream(DB_FILE);
            byte[] mBuffer = new byte[1024];
            int mLength;
            while ((mLength = mInput.read(mBuffer)) > 0) {
                mOutput.write(mBuffer, 0, mLength);
            }
            mOutput.flush();
            mOutput.close();
            mInput.close();
        }

        // Open the database, so we can query it
        public void openDataBase() throws SQLException {
            mDataBase = SQLiteDatabase.openDatabase(String.valueOf(DB_FILE), null, SQLiteDatabase.NO_LOCALIZED_COLLATORS);
        }

        @Override
        public synchronized void close() {
            if(mDataBase != null) {
                mDataBase.close();
            }
            super.close();
        }

        @Override
        public void onCreate(SQLiteDatabase db) {

        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

        }

    }
}
