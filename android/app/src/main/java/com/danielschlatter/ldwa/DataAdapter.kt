package com.danielschlatter.ldwa

import android.content.ContentValues
import android.content.Context
import android.database.Cursor
import android.database.SQLException
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.util.Log
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.io.OutputStream

open class DataAdapter(context: Context) {
    private var mDb: SQLiteDatabase? = null
    private val mDbHelper: DataBaseHelper = DataBaseHelper(context)

    @Throws(SQLException::class)
    fun createDatabase() {
        try {
            mDbHelper.createDataBase()
        } catch (mIOException: IOException) {
            Log.e(TAG, "$mIOException  UnableToCreateDatabase")
            throw Error("UnableToCreateDatabase")
        }
    }

    @Throws(SQLException::class)
    fun open() {
        mDb = try {
            mDbHelper.openDataBase()
            mDbHelper.close()
            mDbHelper.readableDatabase
        } catch (mSQLException: SQLException) {
            Log.e(TAG, "open >>$mSQLException")
            throw mSQLException
        }
    }

    fun selectAll(): Cursor {
        return try {
            mDb!!.rawQuery("select * from weapons order by name", null)
        } catch (mSQLException: SQLException) {
            Log.e(TAG, "selectall failed $mSQLException")
            throw mSQLException
        }
    }

    fun selectPerk(name: String): String {
        return try {
            val mCur = mDb!!.rawQuery(
                "select displayProperties_icon from perks where displayProperties_name = ?",
                arrayOf(name)
            )
            mCur.moveToNext()
            val path = mCur.getString(mCur.getColumnIndex("displayProperties_icon"))
            mCur.close()
            path.substring(25, path.length - 4).replace('/', '_')
        } catch (mSQLException: SQLException) {
            Log.e(TAG, "selectperk failed$mSQLException$name")
            throw mSQLException
        }
    }

    fun insertRoll(weapon: String?, p1: Int, p2: Int, p3: Int, p4: Int) {
        val cv = ContentValues()
        cv.put("weapon", weapon)
        cv.put("p1", p1)
        cv.put("p2", p2)
        cv.put("p3", p3)
        cv.put("p4", p4)
        mDb!!.insert("saved_rolls", null, cv)
    }

    fun removeRoll(weapon: String, p1: Int, p2: Int, p3: Int, p4: Int) {
        mDb!!.delete(
            "saved_rolls",
            "weapon = ? and p1 = ? and p2 = ? and p3 = ? and p4 = ?",
            arrayOf(weapon, p1.toString(), p2.toString(), p3.toString(), p4.toString())
        )
    }

    fun selectRolls(weapon: String): Cursor {
        return mDb!!.rawQuery("select * from saved_rolls where weapon = ?", arrayOf(weapon))
    }

    private class DataBaseHelper(context: Context) :
        SQLiteOpenHelper(context, DB_NAME, null, DB_VERSION) {
        private val dbFile: File = context.getDatabasePath(DB_NAME)
        private var mDataBase: SQLiteDatabase? = null
        private val mContext: Context = context

        @Throws(IOException::class)
        fun createDataBase() {
            // If the database does not exist, copy it from the assets.
            val mDataBaseExist = checkDataBase()
            if (!mDataBaseExist) {
                this.readableDatabase
                close()

                // Copy the database from assets
                copyDataBase()
                Log.e(TAG, "createDatabase database created")
                openDataBase()
                try {
                    mDataBase!!.execSQL("create table saved_rolls(weapon text, p1 int, p2 int, p3 int, p4 int)")
                } catch (mSQLException: SQLException) {
                    Log.e(TAG, "table select_rolls creation failed >>$mSQLException")
                    throw mSQLException
                }
            }
        }

        // Check that the database file exists in databases folder
        private fun checkDataBase(): Boolean {
            return dbFile.exists()
        }

        // Copy the database from assets
        @Throws(IOException::class)
        private fun copyDataBase() {
            val mInput = mContext.assets.open(DB_NAME)
            val mOutput: OutputStream = FileOutputStream(dbFile)
            val mBuffer = ByteArray(1024)
            var mLength: Int
            while (mInput.read(mBuffer).also { mLength = it } > 0) {
                mOutput.write(mBuffer, 0, mLength)
            }
            mOutput.flush()
            mOutput.close()
            mInput.close()
        }

        // Open the database, so we can query it
        @Throws(SQLException::class)
        fun openDataBase() {
            mDataBase = SQLiteDatabase.openDatabase(
                dbFile.toString(),
                null,
                SQLiteDatabase.NO_LOCALIZED_COLLATORS
            )
        }

        @Synchronized
        override fun close() {
            if (mDataBase != null) {
                mDataBase!!.close()
            }
            super.close()
        }

        override fun onCreate(db: SQLiteDatabase) {}
        override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {}

        companion object {
            private const val TAG = "DataBaseHelper" // Tag just for the LogCat window
            private const val DB_NAME = "weapons_database.sqlite" // Database name
            private const val DB_VERSION = 1 // Database version
        }

    }

    companion object {
        protected const val TAG = "DataAdapter"
    }

}