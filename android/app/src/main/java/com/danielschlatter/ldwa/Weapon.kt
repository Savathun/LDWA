package com.danielschlatter.ldwa

import java.util.*

class Weapon(
    var id: Int,
    var name: String,
    val type: String,
    val archetype: String,
    private val icon: String,
    private val ammo_icon: String,
    val synergy: String,
    val perk_column_1: String,
    val perk_column_2: String,
    val perk_column_3: String,
    val perk_column_4: String,
    private val screenshot: String,
    private val element_icon: String
) {
    fun getIcon(): String {
        return icon.substring(25, icon.length - 4).replace('/', '_')
    }

    fun getAmmoIcon(): String {
        return ammo_icon.substring(25, ammo_icon.length - 4).replace('/', '_')
    }

    fun getScreenshot(): String {
        return screenshot.substring(25, screenshot.length - 4).replace('/', '_')
    }

    fun getElementIcon(): String {
        return element_icon.substring(25, element_icon.length - 4).replace('/', '_')
            .lowercase(Locale.getDefault())
    }
}