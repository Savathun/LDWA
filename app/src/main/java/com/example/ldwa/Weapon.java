package com.example.ldwa;

public class Weapon {
    private int id;
    private String name, type, archetype, icon, element, slot, ammo, ammo_icon, synergy, perk_column_1,
            perk_column_2, perk_column_3, perk_column_4, screenshot, element_icon;

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getArchetype() {
        return archetype;
    }

    public void setArchetype(String archetype) {
        this.archetype = archetype;
    }

    public String getIcon() {
        return icon.substring(25, icon.length()-4).replace('/', '_');
    }

    public void setIcon(String icon) {
        this.icon = icon;
    }

    public String getElement() {
        return element;
    }

    public void setElement(String element) {
        this.element = element;
    }

    public String getSlot() {
        return slot;
    }

    public void setSlot(String slot) {
        this.slot = slot;
    }

    public String getAmmo() {
        return ammo;
    }

    public void setAmmo(String ammo) {
        this.ammo = ammo;
    }

    public String getAmmo_icon() {
        return ammo_icon.substring(25, ammo_icon.length()-4).replace('/', '_');
    }

    public void setAmmo_icon(String ammo_icon) {
        this.ammo_icon = ammo_icon;
    }

    public String getSynergy() {
        return synergy;
    }

    public void setSynergy(String synergy) {
        this.synergy = synergy;
    }

    public String getPerk_column_1() {
        return perk_column_1;
    }

    public void setPerk_column_1(String perk_column_1) {
        this.perk_column_1 = perk_column_1;
    }

    public String getPerk_column_2() {
        return perk_column_2;
    }

    public void setPerk_column_2(String perk_column_2) {
        this.perk_column_2 = perk_column_2;
    }

    public String getPerk_column_3() {
        return perk_column_3;
    }

    public void setPerk_column_3(String perk_column_3) {
        this.perk_column_3 = perk_column_3;
    }

    public String getPerk_column_4() {
        return perk_column_4;
    }

    public void setPerk_column_4(String perk_column_4) {
        this.perk_column_4 = perk_column_4;
    }

    public String getScreenshot() {
        return screenshot.substring(25, screenshot.length()-4).replace('/', '_');
    }

    public void setScreenshot(String screenshot) {
        this.screenshot = screenshot;
    }

    public String getElement_icon() {
        return element_icon.substring(25, element_icon.length()-4).replace('/', '_').toLowerCase();
    }

    public void setElement_icon(String element_icon) {
        this.element_icon = element_icon;
    }
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getId () {
        return id;
    }

    public void setId (int id) {
        this.id = id;
    }

    public Weapon(int id, String name, String type, String archetype, String icon,
                  String element, String slot, String ammo, String ammo_icon, String synergy,
                  String perk_column_1, String perk_column_2, String perk_column_3,
                  String perk_column_4, String screenshot, String element_icon) {
        this.id = id;
        this.name = name;
        this.type = type;
        this.archetype = archetype;
        this.icon = icon;
        this.element = element;
        this.slot = slot;
        this.ammo = ammo;
        this.ammo_icon = ammo_icon;
        this.synergy = synergy;
        this.perk_column_1 = perk_column_1;
        this.perk_column_2 = perk_column_2;
        this.perk_column_3 = perk_column_3;
        this.perk_column_4 = perk_column_4;
        this.screenshot = screenshot;
        this.element_icon = element_icon;
    }


}