'use strict';
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#nav-links');
if (menu && navigation) {
  menu.hidden = false;
  document.documentElement.classList.add('js');
  const closeMenu = () => { menu.setAttribute('aria-expanded', 'false'); navigation.classList.remove('is-open'); };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); } });
  navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('click', event => { if (!event.target.closest('.navbar')) closeMenu(); });
  window.matchMedia('(max-width: 768px)').addEventListener('change', closeMenu);
}
const filters = document.querySelector('.filters');
if (filters) {
  filters.hidden = false;
  filters.addEventListener('click', event => {
    const selected = event.target.closest('[data-filter]');
    if (!selected) return;
    filters.querySelectorAll('button').forEach(button => {
      const active = button === selected;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    let count = 0;
    document.querySelectorAll('.project-card').forEach(card => {
      card.hidden = selected.dataset.filter !== 'all' && card.dataset.category !== selected.dataset.filter;
      if (!card.hidden) count++;
    });
    document.querySelector('#filter-status').textContent = count + ' proyectos visibles.';
  });
}
const form = document.querySelector('#contact-form');
if (form) {
  form.querySelector('button[type="submit"]').disabled = false;
  const status = document.querySelector('#form-status');
  const validate = field => {
    const value = field.value.trim();
    let error = '';
    if (field.name === 'nombre' && !value) error = 'Escribe tu nombre.';
    if (field.name === 'correo' && (!value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || field.validity.typeMismatch)) error = 'Escribe un correo válido, por ejemplo: tu@correo.com.';
    if (field.name === 'mensaje' && value.length < 10) error = 'Escribe un mensaje de al menos 10 caracteres.';
    document.getElementById(field.id + '-error').textContent = error;
    field.setAttribute('aria-invalid', String(Boolean(error)));
    return !error;
  };
  const fields = Array.from(form.querySelectorAll('input, textarea'));
  fields.forEach(field => field.addEventListener('input', () => {
    status.textContent = '';
    if (field.hasAttribute('aria-invalid')) validate(field);
  }));
  form.addEventListener('submit', event => {
    event.preventDefault();
    const valid = fields.map(validate).every(Boolean);
    status.textContent = valid ? '¡Mensaje validado! Esta es una demostración: no se envió ni guardó información.' : 'Revisa los campos indicados antes de continuar.';
    if (!valid) fields.find(field => field.getAttribute('aria-invalid') === 'true').focus();
  });
}
