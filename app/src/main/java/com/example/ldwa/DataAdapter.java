package com.example.ldwa;

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

    private final Context mContext;
    private SQLiteDatabase mDb;
    private DataBaseHelper mDbHelper;

    public DataAdapter(Context context) {
        this.mContext = context;
        mDbHelper = new DataBaseHelper(mContext);
    }

    public DataAdapter createDatabase() throws SQLException {
        try {
            mDbHelper.createDataBase();
        } catch (IOException mIOException) {
            Log.e(TAG, mIOException.toString() + "  UnableToCreateDatabase");
            throw new Error("UnableToCreateDatabase");
        }
        return this;
    }

    public DataAdapter open() throws SQLException {
        try {
            mDbHelper.openDataBase();
            mDbHelper.close();
            mDb = mDbHelper.getReadableDatabase();
        } catch (SQLException mSQLException) {
            Log.e(TAG, "open >>"+ mSQLException.toString());
            throw mSQLException;
        }
        return this;
    }

    public void close() {
        mDbHelper.close();
    }

    public Cursor selectAll() {
        try {
            Cursor mCur = mDb.rawQuery("select * from weapons order by name", null);
            if (mCur != null) {
                mCur.moveToNext();
            }
            return mCur;
        } catch (SQLException mSQLException) {
            Log.e(TAG, "getTestData >>"+ mSQLException.toString());
            throw mSQLException;
        }
    }


    private static class DataBaseHelper extends SQLiteOpenHelper {

        private static String TAG = "DataBaseHelper"; // Tag just for the LogCat window
        private static String DB_NAME ="weapons_database.sqlite"; // Database name
        private static int DB_VERSION = 1; // Database version
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
        public boolean openDataBase() throws SQLException {
            // Log.v("DB_PATH", DB_FILE.getAbsolutePath());
            // mDataBase = SQLiteDatabase.openDatabase(DB_FILE, SQLiteDatabase.CREATE_IF_NECESSARY);
            mDataBase = SQLiteDatabase.openDatabase(String.valueOf(DB_FILE), null, SQLiteDatabase.NO_LOCALIZED_COLLATORS);
            return mDataBase != null;
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
