package com.danielschlatter.ldwa;

public class Weapon {
    private int id;
    private String name;
    private final String type;
    private final String archetype;
    private final String icon;
    private final String element;
    private final String slot;
    private final String ammo;
    private final String ammo_icon;
    private final String synergy;
    private final String perk_column_1;
    private final String perk_column_2;
    private final String perk_column_3;
    private final String perk_column_4;
    private final String screenshot;
    private final String element_icon;

    public String getType() {
        return type;
    }

    public String getArchetype() {
        return archetype;
    }

    public String getIcon() {
        return icon.substring(25, icon.length()-4).replace('/', '_');
    }

    public String getElement() {
        return element;
    }

    public String getSlot() {
        return slot;
    }

    public String getAmmo() {
        return ammo;
    }

    public String getAmmo_icon() {
        return ammo_icon.substring(25, ammo_icon.length()-4).replace('/', '_');
    }

    public String getSynergy() {
        return synergy;
    }

    public String getPerk_column_1() {
        return perk_column_1;
    }

    public String getPerk_column_2() {
        return perk_column_2;
    }

    public String getPerk_column_3() {
        return perk_column_3;
    }

    public String getPerk_column_4() {
        return perk_column_4;
    }

    public String getScreenshot() {
        return screenshot.substring(25, screenshot.length()-4).replace('/', '_');
    }

    public String getElement_icon() {
        return element_icon.substring(25, element_icon.length()-4).replace('/', '_').toLowerCase();
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